from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, APIException
from rest_framework.request import Request

from django.db import transaction

from account.models import User
from account.utils import ValidUserOrReadOnlyPermission, IsSuperUser

from .serializers import CommunitySerializer, OwnershipTransferSerializer, CommunitySimpleSerializer, \
    CommunityJoinSerializer, CommunityNewMemberAuditSerializer, CommunitySysAdminAuditSerializer, \
    CommunityInviteSerializer, get_community_non_members_list, CommunityInvitationSerializer, \
    CommunityJoinResponseSerializer, CommunityCheckListSerializer, CommunityCheckListCreateItemSerializer, \
    CommunityCheckListRemoveItemSerializer, CommunityCheckListSetItemSerializer, CommunityCheckListMoveItemSerializer
from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwner, IsUser
from .models import Community, Invitation
from notice.utils import NoticeManager


class CommunityListView(generics.ListCreateAPIView):
    """
    List all valid communities, and create
    """
    permission_classes = [ValidUserOrReadOnlyPermission]
    serializer_class = CommunitySimpleSerializer
    queryset = Community.objects.filter(valid=True)
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        with transaction.atomic():
            community = serializer.save(creator=self.request.user,
                                        owner=self.request.user)
            community.admins.add(self.request.user)
            community.members.add(self.request.user, through_defaults={'valid': True})
            NoticeManager.create_notice_S_CA(
                related_user=self.request.user,
                description=f'用户 {self.request.user} 申请创建社团 {community.name}'
            )

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }


class CommunityRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update or delete a specific valid community info (modify is for owner only)
    """
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = CommunitySerializer
    parser_classes = [MultiPartParser]

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Community.objects.all()
        else:
            return Community.objects.filter(valid=True)

    def perform_destroy(self, instance: Community) -> None:  # type: ignore
        request: Request = self.request  # type: ignore
        description = str(request.data.get('description'))
        with transaction.atomic():
            NoticeManager.create_notice_C_D(
                related_community=instance,
                description=description
            )
            instance.delete()


class CommunityTransferView(generics.UpdateAPIView):
    """
    Transfer valid community owner to other community admins (for owner only)
    """
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = OwnershipTransferSerializer
    queryset = Community.objects.filter(valid=True)


class CommunityJoinView(APIView):
    """
    A view for joining or leaving valid community
    """
    permission_classes = [ValidUserOrReadOnlyPermission]

    @swagger_auto_schema(responses={
        200: CommunityJoinResponseSerializer
    })
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk, valid=True)
        return Response(community.get_member_status(request.user))

    @swagger_auto_schema(request_body=CommunityJoinSerializer, responses={
        200: CommunityJoinResponseSerializer,
        400: "Parameter 'join' is invalid",
        406: "Unacceptable 'join' action"
    })
    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk, valid=True)
        serializer = CommunityJoinSerializer(data=request.data)
        user_status = community.get_member_status(request.user)
        if serializer.is_valid():
            # fixme: put following validation logic into serializer
            # maybe serializers.SerializerMethodField() is useful here?
            with transaction.atomic():
                admin = community.admins.filter(id=request.user.pk)
                if not admin:
                    if serializer.validated_data['join']:
                        if user_status['member']:
                            raise NotAcceptable(f'你目前已经为社团成员 ({"正式" if user_status["valid"] else "待审核"})')
                        NoticeManager.create_notice_C_AA(request.user, community)
                        community.members.add(request.user)
                    else:
                        if user_status['member']:
                            if request.user != community.owner:
                                community.members.remove(request.user)
                            else:
                                raise NotAcceptable('社团所有者无法直接退出社团。')
                        else:
                            raise NotAcceptable('你不是此社团成员！')
                    return Response(community.get_member_status(request.user))
                else:
                    raise NotAcceptable('社团的管理员用户无法直接修改自己的加入状态。')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityNewMemberAuditView(generics.RetrieveAPIView):
    """
    A view for valid community admins to show new members
    """
    permission_classes = [IsAdmin]
    queryset = Community.objects.filter(valid=True)
    serializer_class = CommunityNewMemberAuditSerializer


class CommunityNewMemberAuditActionView(APIView):
    """
    A view for valid community admins to audit new members. Action: "allow" or "deny"
    """
    permission_classes = [IsAdmin]

    @swagger_auto_schema(responses={
        200: "Done",
        406: "Wrong action parameter."
    })
    def post(self, request, pk, user_id, action):
        community = get_object_or_404(Community, pk=pk, valid=True)
        self.check_object_permissions(request, community)

        if community.members.filter(id=user_id, membership__valid=True):
            raise NotAcceptable('此成员已经通过审核。')
        elif not community.members.filter(id=user_id):
            raise NotAcceptable('此成员不在审核列表上。')

        member = community.membership_set.get(user_id=user_id)
        related_user = community.members.get(id=user_id)
        subtype_ca = 1
        subtype_c_ap = 2
        with transaction.atomic():
            if action == 'allow':
                description = '加入社团请求被通过。'
                NoticeManager.create_notice_CA(related_user, community, subtype_ca, description)
                NoticeManager.create_notice_C_AP(related_user, community, subtype_c_ap)

                member.valid = True
                member.save()
            elif action == 'deny':
                description = '加入社团请求被拒绝。'
                NoticeManager.create_notice_CA(related_user, community, subtype_ca, description)

                member.delete()
            else:
                raise NotAcceptable('错误的操作。')

        return Response(status=status.HTTP_200_OK)


class CommunitySysAdminAuditViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    """
    A view for sysadmin to audit new communities
    """
    permission_classes = [IsSuperUser]
    serializer_class = CommunitySysAdminAuditSerializer
    queryset = Community.objects.all()

    def perform_update(self, serializer):
        with transaction.atomic():
            status = serializer.validated_data['valid']
            community = self.get_object()
            owner = community.owner
            name = community.name
            serializer.save()
            NoticeManager.create_notice_CA(
                related_user=owner,
                related_community=community,
                subtype=0,
                description=f'你的社团 {name} {"目前已经审核通过" if status else "未通过审核。"}'
            )


class CommunityAdminInviteView(generics.RetrieveAPIView):
    """
    A view for valid community admin to show who can invite
    """
    permission_classes = [IsAdmin]
    serializer_class = CommunityInviteSerializer
    queryset = Community.objects.filter(valid=True)


class CommunityAdminSendInvitationView(APIView):
    """
    A view for valid community admin to send invitation to others
    """
    permission_classes = [IsAdmin]

    @swagger_auto_schema(responses={
        200: "Done",
        406: "Not in the invitation list"
    })
    def post(self, request, pk, user_id):
        community = get_object_or_404(Community, pk=pk, valid=True)
        self.check_object_permissions(request, community)
        with transaction.atomic():
            user_list = get_community_non_members_list(community).values_list('id', flat=True)
            if user_id in user_list:
                user = User.objects.get(id=user_id)
                Invitation.objects.create(
                    user=user,
                    community=community
                )
                NoticeManager.create_notice_PC(
                    related_user=user,
                    related_community=community,
                    subtype=0
                )
                return Response(status=status.HTTP_200_OK)
            else:
                raise NotAcceptable('此用户不在可邀请列表中。')


class CommunityUserInvitationViewSet(mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin,
                                     viewsets.GenericViewSet):
    """
    A viewset for users to handle invitations
    """
    permission_classes = [IsUser]
    serializer_class = CommunityInvitationSerializer

    def get_queryset(self):
        return Invitation.objects.filter(user=self.request.user)

    @swagger_auto_schema(responses={
        204: "Done"
    })
    @action(methods=['post'], detail=True)
    def accept(self, request, *args, **kwargs):
        invitation = self.get_object()
        community = invitation.community
        with transaction.atomic():
            community.members.add(invitation.user, through_defaults={'valid': True})
            invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={
        204: "Done"
    })
    @action(methods=['post'], detail=True)
    def deny(self, request, *args, **kwargs):
        invitation = self.get_object()
        with transaction.atomic():
            NoticeManager.create_notice_C_AP(
                related_user=invitation.user,
                related_community=invitation.community,
                subtype=0
            )
            invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommunityUserRemoveView(APIView):
    """
    A view for valid community admin to remove members (except for owner and admins)
    """
    permission_classes = [IsAdmin]

    @swagger_auto_schema(responses={
        204: "Done",
        406: "User is owner or admin, or user is not in community"
    })
    def delete(self, request, pk, user_id):
        community = get_object_or_404(Community, pk=pk, valid=True)
        self.check_object_permissions(request, community)
        with transaction.atomic():
            if community.members.filter(id=user_id):
                user = User.objects.get(id=user_id)
                if community.owner != user and community.is_admin(user) is False:
                    community.members.remove(user)
                    NoticeManager.create_notice_PC(
                        related_user=user,
                        related_community=community,
                        subtype=2
                    )
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    raise NotAcceptable('无法踢出所有者和管理员。')
            else:
                raise NotAcceptable('此用户不在此社团中。')


class CommunityAdminSetView(APIView):
    """
    A view for community owner to set or unset admins. Action: "set" or "unset"
    """
    permission_classes = [IsOwner]

    @swagger_auto_schema(responses={
        200: "Done",
        406: "Wrong action parameter, or user is not in community"
    })
    def post(self, request, pk, user_id, action):
        community = get_object_or_404(Community, pk=pk, valid=True)
        self.check_object_permissions(request, community)
        with transaction.atomic():
            if community.members.filter(id=user_id):
                user = User.objects.get(id=user_id)
                admin_status = community.is_admin(user)
                if action == 'set' and admin_status is False:
                    community.admins.add(user)
                elif action == 'unset' and admin_status is True:
                    community.admins.remove(user)
                else:
                    raise NotAcceptable('错误的操作。')
            else:
                raise NotAcceptable('此用户不在此社团中。')
            return Response(status=status.HTTP_200_OK)


class CommunityCheckListViewSet(mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    serializer_class = CommunityCheckListSerializer
    queryset = Community.objects.filter(valid=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CommunityCheckListSerializer
        elif self.action == 'create_item':
            return CommunityCheckListCreateItemSerializer
        elif self.action == 'remove_item':
            return CommunityCheckListRemoveItemSerializer
        elif self.action == 'move_item':
            return CommunityCheckListMoveItemSerializer
        else:
            return CommunityCheckListSetItemSerializer

    @swagger_auto_schema(responses={
        200: CommunityCheckListSerializer
    })
    @action(detail=True, methods=['POST'])
    def create_item(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contents = serializer.validated_data['contents']
        with transaction.atomic():
            community: Community = self.get_object()
            community.checklist.append((contents, False))
            community.save()
        serializer = CommunityCheckListSerializer(instance=self.get_object())
        return Response(serializer.data)

    @swagger_auto_schema(responses={
        200: CommunityCheckListSerializer
    })
    @action(detail=True, methods=['POST'])
    def remove_item(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        index = serializer.validated_data['index']
        try:
            with transaction.atomic():
                community: Community = self.get_object()
                del community.checklist[index]
                community.save()
        except IndexError:
            raise NotAcceptable('Index out of range')
        serializer = CommunityCheckListSerializer(instance=self.get_object())
        return Response(serializer.data)

    @swagger_auto_schema(responses={
        200: CommunityCheckListSerializer
    })
    @action(detail=True, methods=['POST'])
    def set_item(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        done = serializer.validated_data['done']
        index = serializer.validated_data['index']
        try:
            with transaction.atomic():
                community: Community = self.get_object()
                community.checklist[index][1] = done
                community.save()
        except IndexError:
            raise NotAcceptable('Index out of range')
        serializer = CommunityCheckListSerializer(instance=self.get_object())
        return Response(serializer.data)

    @swagger_auto_schema(responses={
        200: CommunityCheckListSerializer
    })
    @action(detail=True, methods=['POST'])
    def move_item(self, request, pk):
        """
        Swap two elements
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        index_from = serializer.validated_data['index_from']
        index_to = serializer.validated_data['index_to']
        try:
            with transaction.atomic():
                community: Community = self.get_object()
                community.checklist[index_from], community.checklist[index_to] = \
                    community.checklist[index_to], community.checklist[index_from]
                community.save()
        except IndexError:
            raise NotAcceptable('Index out of range')
        serializer = CommunityCheckListSerializer(instance=self.get_object())
        return Response(serializer.data)
