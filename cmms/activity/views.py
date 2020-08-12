from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .serializers import ActivitySerializer, ActivityUpdateSerializer, ActivitySecretKeySerializer,\
    ActivityOTPSerializer
from .permissions import IsAdminOrReadOnly
from .models import Activity, verify_otp
from account.utils import ValidUserOrReadOnlyPermission, ValidUserPermission
from notice.utils import NoticeManager


# Create your views here.
class ActivityListView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]
    search_fields = ['title', 'description']

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
        with transaction.atomic():
            activity = serializer.save()
            NoticeManager.create_notice_C_AN(activity, subtype=0)


class ActivityDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityUpdateSerializer
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]
    queryset = Activity.objects.all()

    def perform_update(self, serializer):
        with transaction.atomic():
            activity = serializer.save()
            NoticeManager.create_notice_C_AN(activity.related_community, subtype=1)


class ActivitySecretKeyView(generics.RetrieveAPIView):
    serializer_class = ActivitySecretKeySerializer
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]
    queryset = Activity.objects.all()


class ActivitySignInView(generics.GenericAPIView):
    serializer_class = ActivityOTPSerializer
    queryset = Activity.objects.all()
    permission_classes = [ValidUserPermission]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        activity = self.get_object()
        if not activity.related_community.members.filter(id=user.id).exists():
            return JsonResponse({'user': 'not a member of the community'}, status=400)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            if verify_otp(activity.secret_key, otp):
                activity.signed_in_users.add(user)
                return JsonResponse({}, status=200)
            else:
                return JsonResponse({'otp': 'wrong otp'}, status=400)
        else:
            return JsonResponse(serializer.errors, status=400)
