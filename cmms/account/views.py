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
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings

from .models import User


class BaseLoginView(View):
    """
    BaseLoginView is a View supporting traditional login (through username and password)
    """
    backend = 'django.contrib.auth.backends.ModelBackend'
    template_name: str
    template_context = None

    def get(self, request):
        # return TemplateResponse(request, self.template_name, self.template_context)
        return HttpResponse("?")

    def post(self, request):
        if self.check_code():
            self.login()
        return HttpResponse("?")

    def check_code(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if authenticate(self.request, username=username, password=password):
            return True
        # messages.error(self.request, '校验码错误')
        return False

    def login(self, **kwargs):
        if kwargs.get("get_or_create"):
            user, _ = User.objects.get_or_create(
                gid=kwargs.get("gid"),
                student_id=kwargs.get("student_id")
            )
        else:
            user = User.objects.get(
                student_id=kwargs.get("username")
            )
        login(self.request, user, self.backend)


class CASLoginView(BaseLoginView):
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
            self.login(gid=self.gid, student_id=self.student_id, get_or_create=True)
        return HttpResponse("OK!")

    def post(self, request):
        return "#TODO: Decline POST on CAS Login"

    def check_ticket(self):
        if not settings.CAS_PROXY_PAGE:
            service = urlencode({'service': self.service, 'ticket': self.ticket})
        else:
            service = urlencode({'service': settings.CAS_PROXY_PAGE, 'ticket': self.ticket})
        with urlopen(f'{settings.CAS_SERVICE_URL}/serviceValidate?{service}') as req:
            tree = ElementTree.fromstring(req.read())[0]
        cas = '{http://www.yale.edu/tp/cas}'
        if tree.tag != cas + 'authenticationSuccess':
            # messages.error(self.request, '登录失败')
            print("CAS 验证失败。")
            return False
        self.gid = tree.find('attributes').find(cas + 'gid').text.strip()
        self.student_id = tree.find(cas + 'user').text.strip()
        return True


class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponse("注销成功。注意：此操作不会将您从 CAS 服务器上注销。")
