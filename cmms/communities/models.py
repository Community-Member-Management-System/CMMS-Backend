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
    name = models.CharField(
        max_length=64,
        verbose_name=_('社团名称'),
        unique=True
    )
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
    valid = models.BooleanField(default=False, verbose_name=_('社团是否通过审核'))

    def get_member_status(self, user):
        """
        判断某个用户在社团中的情况。
        :param user: 一般为 request.user
        :return: {'member': 是否在 membership 中, 'valid': 是否有效}
        """
        if self.membership_set.filter(user=user).exists():
            member = True
            valid = self.membership_set.get(user=user).valid
        else:
            member = False
            valid = False
        return {
            'member': member,
            'valid': valid
        }


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
    valid = models.BooleanField(default=False, verbose_name=_('成员是否通过审核'))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'community'], name='user_community_unique')
        ]
