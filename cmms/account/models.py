from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Reference: django.contrib.auth.models.UserManager
    """
    def create_user(self, gid, student_id, password=None, **extra_fields):
        user = self.model(gid=gid, student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, gid, student_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(gid, student_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A great documentation by Django about custom user model:
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model
    """
    gid = models.CharField(_("GID"), max_length=16, primary_key=True)
    student_id = models.CharField(_("学号"), max_length=10, unique=True)
    actual_name = models.CharField(_("真实姓名"), max_length=16)
    nick_name = models.CharField(_("昵称"), max_length=64)
    email = models.EmailField(_("Email"), unique=True, blank=True, null=True)
    phone = models.CharField(_("手机号"), max_length=32, blank=True)
    profile = models.TextField(_("个人简介"), blank=True)
    avatar_url = models.URLField(_("头像"), blank=True)
    date_joined = models.DateTimeField(_('注册时间'), default=timezone.now)
    last_login = models.DateTimeField(_('上次登录时间'), blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('对 admin/ 管理页的只读权限'),
    )  # for compatibility with Django Admin

    USERNAME_FIELD = 'gid'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['student_id']

    objects = UserManager()

    def get_full_name(self):
        return f"{self.nick_name} ({self.actual_name}, {self.student_id})"
