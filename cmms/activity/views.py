from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .serializers import ActivitySerializer
from .permissions import IsAdminOrReadOnly
from .models import Activity
from account.utils import ValidUserOrReadOnlyPermission
from notice.utils import NoticeManager


# Create your views here.
class ActivityListView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]

    def get_queryset(self):
        community = self.request.query_params.get('community', None)
        only_mine = self.request.query_params.get('only_mine', None)
        if only_mine is not None and self.request.user.is_authenticated:
            queryset = Activity.objects.none()
            for c in self.request.user.communities_joined.all():
                queryset = c.activity_set.all() | queryset
            return queryset

        if community is None:
            return Activity.objects.all()
        return Activity.objects.filter(related_community__pk=community).all()

    def perform_create(self, serializer):
        activity = serializer.save()
        NoticeManager.create_notice_C_AN(activity.related_community, '新的活动创建')


class ActivityDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]
    queryset = Activity.objects.all()

    def perform_update(self, serializer):
        activity = serializer.save()
        NoticeManager.create_notice_C_AN(activity.related_community, '活动信息已被更新')
