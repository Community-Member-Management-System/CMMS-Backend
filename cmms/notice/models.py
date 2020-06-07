from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from . import NoticeType


class Notice(models.Model):
    date = models.DateTimeField(default=timezone.now, verbose_name=_('通知时间'))
    type = models.IntegerField(verbose_name=_('通知类型'))
    related_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     verbose_name=_('关联用户'),
                                     null=True)
    related_community = models.ForeignKey(settings.COMMUNITY_MODEL,
                                          on_delete=models.CASCADE,
                                          verbose_name=_('关联社团'),
                                          null=True)

    # TODO: Comment
    # related_comment = models.ForeignKey("Comment",
    #                                     on_delete=models.CASCADE,
    #                                     verbose_name=_('关联评论'),
    #                                     null=True)

    subtype = models.IntegerField(verbose_name=_('通知子类型'), null=True)
    description = models.TextField(verbose_name=_('通知描述'),
                                   blank=True,
                                   null=True)


class NoticeBox(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name=_('用户'),
                             null=True)
    notice = models.ForeignKey(Notice,
                               on_delete=models.CASCADE,
                               verbose_name=_('通知'),
                               null=True)
    read = models.BooleanField(default=False, verbose_name=_('已读'))
