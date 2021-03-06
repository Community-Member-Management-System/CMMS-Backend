"""
Why not django-cas-ng? As it cannot handle USTC CAS's service limitation.
USTC CAS validates service parameter, and "localhost" is NOT accepted, even on CAS test server.

This following code about CAS and traditional login is modified from ustclug/hackergame
(MIT License, Author = HyperCube)

cas.html (CAS_PROXY_PAGE) is from https://github.com/zzh1996/ustccas-revproxy/blob/master/cas_redirect.html
"""
from typing import List, Sequence, Type
from urllib.parse import urlencode
from urllib.request import urlopen
from xml.etree import ElementTree

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins, viewsets, generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from communities.models import Community
from activity.models import Activity
from .models import User
from .serializers import PublicUserInfoSerializer, CurrentUserInfoSerializer, UserCheckSerializer, DetailSerializer, \
    LoginSerializer, LoginResponseSerializer, LimitedFilterResponseSerializer
from .utils import is_new_user, UserInfoPermission, is_super_user
from .token import get_tokens_for_user


class BaseLoginView(APIView):
    """
    BaseLoginView is a View supporting traditional login (through username and password)
    This view supports POST.
    """
    backend = 'django.contrib.auth.backends.ModelBackend'
    template_name: str
    template_context = None
    permission_classes: Sequence[Type[BasePermission]] = []

    @swagger_auto_schema(request_body=LoginSerializer, responses={
        200: "JWT Response",
        401: DetailSerializer
    })
    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        if authenticate(self.request, username=username, password=password):
            user = self.login(username=username)
            jwt = get_tokens_for_user(user)
            return Response(jwt)
        return Response({
            "detail": "登录失败。"
        }, status=status.HTTP_401_UNAUTHORIZED)

    def login(self, **kwargs) -> User:
        if kwargs.get("get_or_create"):
            user, created = User.objects.get_or_create(
                gid=kwargs.get("gid"),
                student_id=kwargs.get("student_id")
            )
        else:
            user = User.objects.get(
                student_id=kwargs.get("username")
            )
        login(self.request, user, self.backend)
        return user


class CASLoginView(BaseLoginView):
    """
    CASLoginView inherits from BaseLoginView, with CAS support.
    This view supports GET (intended for a <a href="..."></a> tag), as it needs 302 to CAS server.
    """
    service: str
    ticket: str
    gid: str
    student_id: str
    permission_classes: Sequence[Type[BasePermission]] = []

    @swagger_auto_schema(responses={
        302: 'Redirect to USTC CAS Server, or redirect to / (and set cookie "refresh", "access" and "login=true")',
        401: 'CAS Login failure'
    })
    def get(self, request):
        self.service = request.build_absolute_uri()
        self.ticket = request.GET.get('ticket')
        if not settings.CAS_PROXY_PAGE:
            service = self.service
        else:
            service = f"{settings.CAS_PROXY_PAGE}?{urlencode({'jump': self.service})}"
        if not self.ticket:
            return redirect(f'{settings.CAS_SERVICE_URL}/login?{urlencode({"service": service})}')
        if self.check_ticket():
            user = self.login(gid=self.gid, student_id=self.student_id, get_or_create=True)
            jwt = get_tokens_for_user(user)
            response = redirect(request.GET.get('next', '/'))
            response.set_cookie('refresh', jwt['refresh'])
            response.set_cookie('access', jwt['access'])
            response.set_cookie('login', 'true')
            response.set_cookie('cas', 'true')
            return response
        return HttpResponse("登录失败。<a href='/'>返回主页</a>",
                            status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        return HttpResponseNotAllowed(["GET"])

    def check_ticket(self) -> bool:
        if not settings.CAS_PROXY_PAGE:
            service = urlencode({'service': self.service, 'ticket': self.ticket})
        else:
            service = urlencode({'service': settings.CAS_PROXY_PAGE, 'ticket': self.ticket})
        with urlopen(f'{settings.CAS_SERVICE_URL}/serviceValidate?{service}') as req:
            tree = ElementTree.fromstring(req.read())[0]
        cas = '{http://www.yale.edu/tp/cas}'
        if tree.tag != cas + 'authenticationSuccess':
            return False
        try:
            # let mypy ignores here, as we have try-except AttributeError
            self.gid = tree.find('attributes').find(cas + 'gid').text.strip()  # type: ignore
            self.student_id = tree.find(cas + 'user').text.strip()  # type: ignore
            return True
        except AttributeError:
            # there's something wrong with ElementTree.find()
            return False


class LogoutView(APIView):
    """
    Logout (POST)
    """
    permission_classes: Sequence[Type[BasePermission]] = []

    @swagger_auto_schema(responses={
        200: DetailSerializer
    })
    def post(self, request):
        logout(request)
        response_dict = {
            'detail': '注销成功。'
        }
        if request.COOKIES.get('cas', None):
            service = request.build_absolute_uri('/')
            if settings.CAS_PROXY_PAGE:
                service = f"{settings.CAS_PROXY_PAGE}?{urlencode({'jump': service})}"
            response_dict['cas_logout'] = f'{settings.CAS_SERVICE_URL}/logout?{urlencode({"service": service})}'
        response = Response(response_dict)
        response.delete_cookie('refresh')
        response.delete_cookie('access')
        response.delete_cookie('login')
        response.delete_cookie('cas')
        return response


class LoginCheckView(APIView):
    """
    A view for checking current user status
    """
    permission_classes: Sequence[Type[BasePermission]] = []

    @swagger_auto_schema(responses={
        200: UserCheckSerializer
    })
    def post(self, request):
        return Response({
            "login": request.user.is_authenticated,
            "new": None if not request.user.is_authenticated else is_new_user(request.user),
            "userid": None if not request.user.is_authenticated else request.user.id,
            "superuser": request.user.is_superuser
        })


@method_decorator(name='update', decorator=swagger_auto_schema(
    request_body=CurrentUserInfoSerializer
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    request_body=CurrentUserInfoSerializer
))
class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    List, Retrieve and update user info. See PublicUserInfo and CurrentUserInfo (below) for response format.
    """
    queryset = User.objects.all()
    permission_classes = [UserInfoPermission]
    parser_classes = [MultiPartParser]
    search_fields = ['nick_name', 'profile']

    def get_serializer_class(self):
        if is_super_user(self.request.user):
            return CurrentUserInfoSerializer
        if self.action == 'list':
            return PublicUserInfoSerializer
        try:
            user: User = self.get_object()
            if user == self.request.user:
                return CurrentUserInfoSerializer
            else:
                return PublicUserInfoSerializer
        except AssertionError:
            # fix complaining drf-yasg
            return PublicUserInfoSerializer


class LimitedGetUserByStudentIDView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, description="学号", type=openapi.TYPE_STRING),
        openapi.Parameter('activity_id', openapi.IN_QUERY, description="活动 ID", type=openapi.TYPE_INTEGER),
    ], responses={
        200: LimitedFilterResponseSerializer,
        404: '找不到学号或社团',
        403: '非对应社团管理员'
    })
    def get(self, request):
        requester = request.user
        student_id = request.query_params.get('student_id')
        activity_id = request.query_params.get('activity_id')
        user_id = request.query_params.get('user_id')
        print(student_id, activity_id)
        activity = get_object_or_404(Activity, id=activity_id)
        if student_id:
            user = get_object_or_404(User, student_id=student_id)
        else:
            user = get_object_or_404(User, id=user_id)
        community = activity.related_community
        if community.is_admin(requester) is False:
            raise PermissionDenied
        member_status = community.get_member_status(user)
        if member_status['member'] is True and member_status['valid'] is True:
            # in club
            return Response({
                'user_id': user.id,
                'nick_name': user.nick_name,
                'real_name': user.real_name,
                'phone': user.phone,
                'email': user.email,
                'student_id': user.student_id
            })
        else:
            # out of club
            return Response({
                'user_id': user.id,
                'nick_name': user.nick_name,
                'real_name': None,
                'phone': None,
                'email': None,
                'student_id': user.student_id
            })
