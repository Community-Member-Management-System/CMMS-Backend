from .models import Notice, NoticeBox
from django.conf import settings
from django.utils import timezone
from django.http import Http404
from account.models import User
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from django.db.models.query import QuerySet
from communities.models import Community
from activity.models import Activity, Comment


class NoticeManager:
    __notice_manager = Notice.objects
    __notice_box_manager = NoticeBox.objects
    __user_manager = User.objects
    __C_AN_subtype_map = {0: '创建了', 1: '更新了', 2: '删除了'}

    # NoticeBox 条目获取和鉴权
    @classmethod
    def __get_notice_box(cls, user: User, pk: int) -> NoticeBox:
        queryset = cls.__notice_box_manager.filter(pk=pk)
        if queryset.count() == 0:
            raise Http404
        else:
            object = queryset.get(pk=pk)
            if object.user != user:
                raise Http404
            elif object.deleted:
                raise Http404
            else:
                return object

    # 生成邮件内容
    @classmethod
    def __create_email_subject(cls, community: Community, subtype: int, title: str) -> str:
        header = community.name + '社团管理员' + cls.__C_AN_subtype_map[
            subtype] + '活动：'
        return settings.DEFAULT_EMAIL_PREFIX + header + title

    @classmethod
    def __create_email_message(cls, activity: Activity) -> str:
        content = '开始时间：' + str(activity.start_time) \
            + '\n结束时间：' + str(activity.end_time) \
            + '\n活动地点：' + activity.location \
            + '\n活动提要：' + activity.description \
            + '\n'
        return content

    # 分类对 NoticeBox 更新
    @classmethod
    def __create_notice_P(cls, user: User, notice: Notice) -> None:
        cls.__notice_box_manager.create(user=user, notice=notice)

    @classmethod
    def __create_notice_C(cls, community: Community, notice: Notice) -> None:
        for member in community.members.all():
            user_status = community.get_member_status(member)
            if user_status['valid']:
                cls.__notice_box_manager.create(user=member, notice=notice)

    @classmethod
    def __create_notice_C_A(cls, community: Community, notice: Notice) -> None:
        for admin in community.admins.all():
            cls.__notice_box_manager.create(user=admin, notice=notice, administrative=True)

    @classmethod
    def __create_notice_S(cls, notice: Notice) -> None:
        for superuser in cls.__user_manager.filter(is_superuser=True):
            cls.__notice_box_manager.create(user=superuser, notice=notice, administrative=True)

    # 创建 Notice 的方法
    @classmethod
    def create_notice_PC(cls, related_user: User, related_community: Community, subtype: int) -> None:
        type = 'PC'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_community=related_community,
            subtype=subtype)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_AR(cls, related_user: User, related_comment: Comment, subtype: int) -> None:
        type = 'AR'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_comment=related_comment,
            subtype=subtype)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_CA(cls,
                         related_user: User,
                         related_community: Community,
                         subtype: int,
                         description: str = '') -> None:
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
    def create_notice_B(cls, related_user: User, description: str = '') -> None:
        type = 'B'
        new_notice = cls.__notice_manager.create(type=type,
                                                 related_user=related_user,
                                                 description=description)
        cls.__create_notice_P(related_user, new_notice)

    @classmethod
    def create_notice_C_AN(cls, related_activity: Activity, subtype: int, if_send_mail: bool = False) -> None:
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
                member.email for member in related_community.members.all() if member.email
            ]
            if not recipient_list:
                return
            send_mail(subject=subject,
                      message=message,
                      recipient_list=recipient_list,
                      from_email=settings.DEFAULT_FROM_EMAIL)

    @classmethod
    def create_notice_C_AP(cls,
                           related_user: User,
                           related_community: Community,
                           subtype: int,
                           description: str = '') -> None:
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
                           related_user: User,
                           related_community: Community,
                           description: str = '') -> None:
        type = 'C_AA'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_user=related_user,
            related_community=related_community,
            description='')
        cls.__create_notice_C_A(related_community, new_notice)

    @classmethod
    def create_notice_C_D(cls, related_community: Community, description: str = '') -> None:
        type = 'C_D'
        new_notice = cls.__notice_manager.create(
            type=type,
            related_community=related_community,
            description=description)
        cls.__create_notice_C(related_community, new_notice)

    @classmethod
    def create_notice_S_CA(cls, related_user: User, description: str = '') -> None:
        type = 'S_CA'
        new_notice = cls.__notice_manager.create(type=type,
                                                 related_user=related_user,
                                                 description=description)
        cls.__create_notice_S(new_notice)

    # 操作 NoticeBox 的方法
    @classmethod
    def fetch(cls, user: User) -> 'QuerySet[NoticeBox]':
        return cls.__notice_box_manager.filter(user=user, deleted=False)

    @classmethod
    def read(cls, user: User, pk: int) -> None:
        object = cls.__get_notice_box(user, pk)
        object.read = True
        object.save()

    @classmethod
    def unread(cls, user: User, pk: int) -> None:
        object = cls.__get_notice_box(user, pk)
        object.read = False
        object.save()

    @classmethod
    def delete(cls, user: User, pk: int) -> None:
        object = cls.__get_notice_box(user, pk)
        object.deleted = True
        object.save()

    @classmethod
    def access(cls, user: User, pk: int) -> Notice:
        return cls.__get_notice_box(user, pk).notice
