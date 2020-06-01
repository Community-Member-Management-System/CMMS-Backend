"""
Why not django-cas-ng? As it cannot handle USTC CAS's service limitation.
USTC CAS validates service parameter, and "localhost" is NOT accepted, even on CAS test server.

This following code about CAS and traditional login is modified from ustclug/hackergame
(MIT License, Author = HyperCube)

cas.html (CAS_PROXY_PAGE) is from https://github.com/zzh1996/ustccas-revproxy/blob/master/cas_redirect.html
"""
from urllib.parse import urlencode
from urllib.request import urlopen
from xml.etree import ElementTree

from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from rest_framework import status, mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import PublicUserInfoSerializer, CurrentUserInfoSerializer
from .utils import is_new_user


class BaseLoginView(APIView):
    """
    BaseLoginView is a View supporting traditional login (through username and password)
    This view supports POST.
    """
    backend = 'django.contrib.auth.backends.ModelBackend'
    template_name: str
    template_context = None

    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        if authenticate(self.request, username=username, password=password):
            user = self.login(username=username)
            return Response({
                "msg": "登录成功。",
                "new": is_new_user(user),
            })
        return Response({
            "msg": "登录失败。"
        }, status=status.HTTP_401_UNAUTHORIZED)

    def login(self, **kwargs):
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
            return redirect(f"/?login=true&new={'true' if is_new_user(user) else 'false'}")
        return HttpResponse(f"登录失败。<a href='/'>返回主页</a>",
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        return HttpResponseNotAllowed(["GET"])

    def check_ticket(self):
        if not settings.CAS_PROXY_PAGE:
            service = urlencode({'service': self.service, 'ticket': self.ticket})
        else:
            service = urlencode({'service': settings.CAS_PROXY_PAGE, 'ticket': self.ticket})
        with urlopen(f'{settings.CAS_SERVICE_URL}/serviceValidate?{service}') as req:
            tree = ElementTree.fromstring(req.read())[0]
        cas = '{http://www.yale.edu/tp/cas}'
        if tree.tag != cas + 'authenticationSuccess':
            return False
        self.gid = tree.find('attributes').find(cas + 'gid').text.strip()
        self.student_id = tree.find(cas + 'user').text.strip()
        return True


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({
            "msg": "注销成功。注意：此操作不会将您从 CAS 服务器上注销。"
                   f"如果您正在使用公用计算机，请手动至 {settings.CAS_SERVICE_URL}/logout 退出账号。"
        })


class LoginCheckView(APIView):
    def post(self, request):
        return Response({
            "login": request.user.is_authenticated,
            "new": None if not request.user.is_authenticated else is_new_user(request.user)
        })


class ReadOnlyUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple viewset to show user public information
    """
    queryset = User.objects.all()
    serializer_class = PublicUserInfoSerializer


class CurrentUserInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = CurrentUserInfoSerializer

    def get_object(self):
        return self.request.user
