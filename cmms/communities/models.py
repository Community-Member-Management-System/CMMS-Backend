from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
class Community(models.Model):
    creator = models.ForeignKey(
        _('创建者'),
        settings.AUTH_USER_MODEL,
        on_delele=models.SET_NULL,
    )
    # community can be transferred, so owner and creator may differ
    owner = models.ForeignKey(
        _('拥有者'),
        settings.AUTH_USER_MODEL,
        on_delte=models.SET_NULL,
    )
    name = models.CharField(_('社团名称'), max_length=64)
    profile = models.TextField(_('社团简介'), blank=True)
    date_created = models.DateTimeField(_('创建时间'), default=timezone.now)
    members = models.ManyToManyField(
        _('成员'),
        settings.AUTH_USER_MODEL,
        through='Membership',
        through_fields=('community', 'user'),
    )
    admins = models.ManyToManyField(_('管理员'), settings.AUTH_USER_MODEL)


class Membership(models.Model):
    user = models.ForeignKey(
        _('用户'),
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    community = models.ForeignKey(
        _('社团'),
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_joined = models.DateTimeField(_('加入时间'), auto_now_add=True)
