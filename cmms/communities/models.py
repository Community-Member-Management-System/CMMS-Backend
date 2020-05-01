from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
class Community(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('创建者'),
        related_name='communities_created',
    )
    # community can be transferred, so owner and creator may differ
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('拥有者'),
        related_name='communities_owned',
    )
    name = models.CharField(max_length=64, verbose_name=_('社团名称'))
    profile = models.TextField(blank=True, verbose_name=_('社团简介'))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_('创建时间'))
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        through_fields=('community', 'user'),
        verbose_name=_('成员'),
        related_name='communities_joined',
    )
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('管理员'))


class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('用户'),
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name=_('社团'),
    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_('加入时间'))
