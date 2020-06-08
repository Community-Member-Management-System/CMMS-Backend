from .models import Notice, NoticeBox
from django.conf import settings
from django.utils import timezone


class NoticeManager:
    __notice_manager = Notice.objects
    __notice_box_manager = NoticeBox.objects
    __user_manager = settings.AUTH_USER_MODEL.objects

    # 暂时没用
    # __community_manager = settings.COMMUNITY_MODEL.objects

    # TODO: Comment
    # __comment_manager = settings.COMMENT_MODEL.objects

    # 分类对 NoticeBox 更新
    def __create_notice_P(self, user, notice):
        self.__notice_box_manager.create(user, notice)

    def __create_notice_C(self, community, notice):
        for member in community.members.all():
            self.__notice_box_manager.create(member, notice)

    def __create_notice_C_A(self, community, notice):
        for admin in community.admins.all():
            self.__notice_box_manager.create(admin, notice)

    def __create_notice_S(self, notice):
        for staff in self.__user_manager.filter(is_staff=True):
            self.__notice_box_manager.create(staff, notice)

    # 创建 Notice 的方法
    def create_notice_PC(self, related_user, related_community, subtype, date=timezone.now):
        type = 'PC'
        new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, related_community=related_community, subtype=subtype)
        self.__create_notice_P(related_user, new_notice)

    # TODO: Comment
    # def create_notice_AR(self, related_user, related_comment, subtype, date=timezone.now):
    #     type = 'AR'
    #     new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, related_comment=related_comment, subtype=subtype)
    #     self.__create_notice_P(related_user, new_notice)

    def create_notice_CA(self, related_user, related_community, subtype, date=timezone.now):
        type = 'CA'
        if related_community is None:
            new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, subtype=subtype)
        else:
            new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, related_community=related_community, subtype=subtype)
        self.__create_notice_P(related_user, new_notice)

    def create_notice_B(self, related_user, description, date=timezone.now):
        type = 'B'
        new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, description=description)
        self.__create_notice_P(related_user, new_notice)

    def create_notice_C_AN(self, related_community, description, date=timezone.now):
        type = 'C_AN'
        new_notice = self.__notice_manager.create(date=date, type=type, related_community=related_community, description=description)
        self.__create_notice_C(related_community, new_notice)

    def create_notice_C_AP(self, related_user, related_community, subtype, date=timezone.now):
        type = 'C_AP'
        new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, related_community=related_community, subtype=subtype)
        self.__create_notice_C_A(related_community, new_notice)

    def create_notice_C_AA(self, related_user, related_community, description, date=timezone.now):
        type = 'C_AA'
        new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, related_community=related_community, description=description)
        self.__create_notice_C_A(related_community, new_notice)

    def create_notice_C_D(self, related_community, description, date=timezone.now):
        type = 'C_D'
        new_notice = self.__notice_manager.create(date=date, type=type, related_community=related_community, description=description)
        self.__create_notice_C(related_community, new_notice)

    def create_notice_S_CA(self, related_user, description, date=timezone.now):
        type = 'S_CA'
        new_notice = self.__notice_manager.create(date=date, type=type, related_user=related_user, description=description)
        self.__create_notice_S_CA(new_notice)

    # 操作 NoticeBox 的方法
    def fetch(self, user):
        return self.__notice_box_manager.filter(user=user)

    def read(self, user, notice):
        self.__notice_box_manager.get(user=user, notice=notice).read = True

    def unread(self, user, notice):
        self.__notice_box_manager.get(user=user, notice=notice).read = False

    def delete(self, user, notice):
        self.__notice_box_manager.get(user=user, notice=notice).delete = True
