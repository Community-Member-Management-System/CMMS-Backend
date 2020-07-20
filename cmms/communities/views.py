from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable

from django.db import transaction

from account.utils import ValidUserOrReadOnlyPermission

from .serializers import CommunitySerializer, OwnershipTransferSerializer, CommunityDetailSerializer, \
    CommunityJoinSerializer, CommunityNewMemberAuditSerializer
from .permissions import IsOwnerOrReadOnly, IsAdmin
from .models import Community
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


class CommunityRetrieveView(generics.RetrieveAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission]
    serializer_class = CommunitySerializer
    queryset = Community.objects.all()


class CommunityTransferView(generics.UpdateAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = OwnershipTransferSerializer
    queryset = Community.objects.all()


class CommunityInfoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # modify community name & profile
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    serializer_class = CommunityDetailSerializer
    queryset = Community.objects.all()


class CommunityDestroyView(generics.DestroyAPIView):
    permission_classes = [ValidUserOrReadOnlyPermission,
                          IsOwnerOrReadOnly]
    queryset = Community.objects.all()


class CommunityJoinView(APIView):
    permission_classes = [ValidUserOrReadOnlyPermission]

    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        return Response(community.get_member_status(request.user))

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
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
                    return Response(CommunitySerializer(community).data)
                else:
                    raise NotAcceptable('社团的管理员用户无法直接修改自己的加入状态。')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityNewMemberAuditView(generics.RetrieveAPIView):
    permission_classes = [IsAdmin]
    queryset = Community.objects.all()
    serializer_class = CommunityNewMemberAuditSerializer


class CommunityNewMemberAuditActionView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk, user_id, action):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)

        if community.members.filter(id=user_id, membership__valid=True):
            raise NotAcceptable('此成员已经通过审核。')
        elif not community.members.filter(id=user_id):
            raise NotAcceptable('此成员不在审核列表上。')

        member = community.membership_set.get(user_id=user_id)
        if action == 'allow':
            member.valid = True
            member.save()
        elif action == 'deny':
            member.delete()
        else:
            raise NotAcceptable('错误的操作。')

        return Response(CommunityNewMemberAuditSerializer(community).data)
