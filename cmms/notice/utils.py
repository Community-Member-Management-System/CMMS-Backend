from .models import Notice, NoticeBox
from django.conf import settings
from django.utils import timezone
from django.http import Http404
from account.models import User
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class NoticeManager:
    __notice_manager = Notice.objects
    __notice_box_manager = NoticeBox.objects
    __user_manager = User.objects
    __C_AN_subtype_map = {0: '创建了', 1: '更新了', 2: '删除了'}

    # 生成邮件内容
    @classmethod
    def __create_email_subject(cls, community, subtype, title):
        header = community.name + '社团管理员' + cls.__C_AN_subtype_map[
            subtype] + '活动：'
        return settings.DEFAULT_EMAIL_PREFIX + header + title

    @classmethod
    def __create_email_message(cls, activity):
        content = '开始时间：' + activity.start_time \
            + '\n结束时间：' + activity.end_time \
            + '\n活动地点：' + activity.location \
            + '\n活动提要：' + activity.description \
            + '\n'
        return content

    # 分类对 NoticeBox 更新
    @classmethod
    def __create_notice_P(cls, user, notice):
        cls.__notice_box_manager.create(user=user, notice=notice)

    @classmethod
    def __create_notice_C(cls, community, notice):
        for member in community.members.all():
            cls.__notice_box_manager.create(user=member, notice=notice)

    @classmethod
    def __create_notice_C_A(cls, community, notice):
        for admin in community.admins.all():
            cls.__notice_box_manager.create(user=admin, notice=notice)

    @classmethod
    def __create_notice_S(cls, notice):
        for superuser in cls.__user_manager.filter(is_superuser=True):
            cls.__notice_box_manager.create(user=superuser, notice=notice)

    # 创建 Notice 的方法
    @classmethod
    def create_notice_PC(cls, related_user, related_community, subtype):
        type = 'PC'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_community=related_community,
            subtype=subtype)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_AR(cls, related_user, related_comment, subtype):
        type = 'AR'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_comment=related_comment,
            subtype=subtype)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_CA(cls,
                         related_user,
                         related_community,
                         subtype,
                         description=''):
        type = 'CA'
        if related_community is None:
            new_notice = cls.__notice_manager.create(type=type,
                                                     related_user=related_user,
                                                     subtype=subtype,
                                                     description=description)
        else:
            new_notice = cls.__notice_manager.create(
                type=type,
                related_user=related_user,
                related_community=related_community,
                subtype=subtype,
                description=description)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_B(cls, related_user, description=''):
        type = 'B'
        new_notice = cls.__notice_manager.create(type=type,
                                                 related_user=related_user,
                                                 description=description)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_C_AN(cls, related_activity, subtype, if_send_mail=False):
        type = 'C_AN'
        related_community = related_activity.related_community
        new_notice = cls.__notice_manager.create(
            type=type, related_activity=related_activity, subtype=subtype)
        cls.__create_notice_C(related_community, new_notice)

        if settings.ENABLE_EMAIL and if_send_mail:
            subject = cls.__create_email_subject(related_community, subtype,
                                                 related_activity.title)
            message = cls.__create_email_message(related_activity)
            recipient_list = [
                member.email for member in related_community.members.all()
            ]
            send_mail(subject=subject,
                      message=message,
                      recipient_list=recipient_list)

    @classmethod
    def create_notice_C_AP(cls,
                           related_user,
                           related_community,
                           subtype,
                           description=''):
        type = 'C_AP'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_community=related_community,
            subtype=subtype,
            description=description)
        cls.__create_notice_C_A(related_community, new_notice)

    @classmethod
    def create_notice_C_AA(cls,
                           related_user,
                           related_community,
                           description=''):
        type = 'C_AA'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_community=related_community,
            description='')
        cls.__create_notice_C_A(related_community, new_notice)

    @classmethod
    def create_notice_C_D(cls, related_community, description=''):
        type = 'C_D'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_community=related_community,
            description=description)
        cls.__create_notice_C(related_community, new_notice)

    @classmethod
    def create_notice_S_CA(cls, related_user, description=''):
        type = 'S_CA'
        new_notice = cls.__notice_manager.create(type=type,
                                                 related_user=related_user,
                                                 description=description)
        cls.__create_notice_S_CA(new_notice)

    # 操作 NoticeBox 的方法
    @classmethod
    def fetch(cls, user):
        return cls.__notice_box_manager.filter(user=user)

    @classmethod
    def read(cls, notice_box):
        notice_box.read = True

    @classmethod
    def unread(cls, notice_box):
        notice_box.read = False

    @classmethod
    def delete(cls, notice_box):
        notice_box.delete = True

    @classmethod
    def access(cls, user, notice_pk):
        try:
            notice = Notice.objects.get(pk=notice_pk)
            if cls.__notice_box_manager.filter(user=user,
                                               notice=notice).count() == 0:
                raise Http404
            else:
                return notice
        except Notice.DoesNotExist:
            raise Http404
