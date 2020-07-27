from rest_framework import generics, status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, APIException

from django.db import transaction

from account.models import User
from account.utils import ValidUserOrReadOnlyPermission, IsSuperUser

from .serializers import CommunitySerializer, OwnershipTransferSerializer, CommunityDetailSerializer, \
    CommunityJoinSerializer, CommunityNewMemberAuditSerializer, CommunitySysAdminAuditSerializer, \
    CommunityInviteSerializer, get_community_non_members_list, CommunityInvitationSerializer
from .permissions import IsOwnerOrReadOnly, IsAdmin, IsOwner, IsUser
from .models import Community, Invitation
from notice.utils import NoticeManager


class CommunityListView(generics.ListCreateAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission]
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()

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


class CommunityRetrieveView(generics.RetrieveAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission]
    serializer_class = CommunitySerializer
    queryset = Community.objects.filter(valid=True)


class CommunityTransferView(generics.UpdateAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = OwnershipTransferSerializer
    queryset = Community.objects.filter(valid=True)


class CommunityInfoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # modify community name & profile
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = CommunityDetailSerializer
    queryset = Community.objects.filter(valid=True)


class CommunityDestroyView(generics.DestroyAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    queryset = Community.objects.all()


class CommunityJoinView(APIView):
    permission_classes = [ValidUserOrReadOnlyPermission]

    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk, valid=True)
        return Response(community.get_member_status(request.user))

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
                            community.members.remove(request.user)
                        else:
                            raise NotAcceptable('你不是此社团成员！')
                    return Response(community.get_member_status(request.user))
                else:
                    raise NotAcceptable('社团的管理员用户无法直接修改自己的加入状态。')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityNewMemberAuditView(generics.RetrieveAPIView):
    permission_classes = [IsAdmin]
    queryset = Community.objects.filter(valid=True)
    serializer_class = CommunityNewMemberAuditSerializer


class CommunityNewMemberAuditActionView(APIView):
    permission_classes = [IsAdmin]

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

        return Response(CommunityNewMemberAuditSerializer(community).data)


class CommunitySysAdminAuditViewSet(mixins.ListModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
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
    permission_classes = [IsAdmin]
    serializer_class = CommunityInviteSerializer
    queryset = Community.objects.filter(valid=True)


class CommunityAdminSendInvitationView(APIView):
    permission_classes = [IsAdmin]

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
                return Response('success')  # fixme
            else:
                raise NotAcceptable('此用户不在可邀请列表中。')


class CommunityUserInvitationViewSet(mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin,
                                     viewsets.GenericViewSet):
    permission_classes = [IsUser]
    serializer_class = CommunityInvitationSerializer

    def get_queryset(self):
        return Invitation.objects.filter(user=self.request.user)

    @action(methods=['post'], detail=True)
    def accept(self, request, *args, **kwargs):
        invitation = self.get_object()
        community = invitation.community
        with transaction.atomic():
            community.members.add(invitation.user, through_defaults={'valid': True})
            invitation.delete()
        return Response('success')  # fixme

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
        return Response('success')  # fixme
