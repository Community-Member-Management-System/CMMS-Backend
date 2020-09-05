from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, mixins, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from account.models import User
from .serializers import ActivitySerializer, ActivityUpdateSerializer, ActivitySecretKeySerializer, \
    ActivityOTPSerializer, ActivitySignedInSerializer, PostVerActivitySerializer, PostVerActivityUpdateSerializer
from .permissions import IsAdminOrReadOnly, IsAdmin
from .models import Activity, verify_otp
from account.utils import ValidUserOrReadOnlyPermission, ValidUserPermission
from notice.utils import NoticeManager


# Create your views here.
class ActivityListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]
    search_fields = ['title', 'description']

    @swagger_auto_schema(
        responses={
            200: ActivitySerializer
        },
        manual_parameters=[
            openapi.Parameter(
                'community',
                openapi.IN_QUERY,
                description='list activities by community',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'only_mine',
                openapi.IN_QUERY,
                description='only list the activities in which the user joined if the parameter exists',
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

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
            if not activity.related_community.admins.filter(id=self.request.user.id).exists():
                if not self.request.user.is_superuser:
                    raise PermissionDenied
            mail_sent = self.request.data.get('mail', False)
            NoticeManager.create_notice_C_AN(activity, subtype=0, if_send_mail=mail_sent)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostVerActivitySerializer
        else:
            return ActivitySerializer


class ActivityDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly,
                          ValidUserOrReadOnlyPermission]
    queryset = Activity.objects.all()

    def perform_update(self, serializer):
        with transaction.atomic():
            activity = serializer.save()
            mail_sent = self.request.data.get('mail', False)
            NoticeManager.create_notice_C_AN(activity, subtype=1, if_send_mail=mail_sent)

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return PostVerActivityUpdateSerializer
        else:
            return ActivityUpdateSerializer


class ActivitySecretKeyView(generics.RetrieveAPIView):
    serializer_class = ActivitySecretKeySerializer
    permission_classes = [IsAdmin,
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


class ActivitySignedInViewSet(mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    queryset = Activity.objects.all()
    serializer_class = ActivitySignedInSerializer

    @action(detail=False, methods=['POST'])
    def add(self, request, pk, user_id):
        activity: Activity = self.get_object()
        user = get_object_or_404(User, pk=user_id)
        activity.signed_in_users.add(user)
        serializer = self.get_serializer(activity)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def remove(self, request, pk, user_id):
        activity: Activity = self.get_object()
        user = get_object_or_404(User, pk=user_id)
        activity.signed_in_users.remove(user)
        serializer = self.get_serializer(activity)
        return Response(serializer.data)
