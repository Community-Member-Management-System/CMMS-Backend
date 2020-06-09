from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Activity(models.Model):
    related_community = models.ForeignKey(settings.COMMUNITY_MODEL,
                                          on_delete=models.CASCADE,
                                          verbose_name=_('关联社团'))
    created_date = models.DateTimeField(default=timezone.now,
                                        verbose_name=_('创建时间'))
    location = models.TextField(verbose_name=_('活动地点'))
    title = models.TextField(verbose_name=_('活动标题'))
    description = models.TextField(verbose_name=_('活动提要'))
    start_time = models.DateTimeField(verbose_name=_('开始时间'))
    end_time = models.DateTimeField(verbose_name=_('结束时间'))
    signed_in_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             verbose_name=_('签到成员'))


class Comment(models.Model):
    related_activity = models.ForeignKey(settings.ACTIVITY_MODEL,
                                         on_delete=models.CASCADE,
                                         verbose_name=_('关联活动'))
    related_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     verbose_name=_('关联用户'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('评论时间'))
    title = models.TextField(verbose_name=_('评论标题'))
    content = models.TextField(verbose_name=_('评论内容'))
