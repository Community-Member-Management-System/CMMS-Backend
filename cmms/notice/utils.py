from .models import Notice, NoticeBox
from django.conf import settings
from django.utils import timezone


class NoticeManager:
    __notice_manager = Notice.objects
    __user_manager = settings.AUTH_USER_MODEL.objects
    __community_manager = settings.COMMUNITY_MODEL.objects

    # TODO: Comment
    # __comment_manager = settings.COMMENT_MODEL.objects

    def __create_notice_P(self, user, notice):
        NoticeBox.objects.create(user, notice)

    def __create_notice_C(self, community, notice):
        for member in community.members.all():
            NoticeBox.objects.create(member, notice)

    def __create_notice_C_A(self, community, notice):
        for admin in community.admins.all():
            NoticeBox.objects.create(admin, notice)

    def __create_notice_S(self, notice):
        for staff in self.__user_manager.filter(is_staff=True):
            NoticeBox.objects.create(staff, notice)

    def create_notice_PC(self, related_user, related_community, subtype, date=timezone.now):
        type = 'PC'
        new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, related_community=related_community, subtype=subtype)
        self.__create_notice_P(related_user, new_notice)

    # TODO: Comment
    # def create_notice_AR(self, related_user, related_comment, subtype, date=timezone.now):
    #     type = 'AR'
    #     new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, related_comment=related_comment, subtype=subtype)
    #     self.__create_notice_P(related_user, new_notice)

    def create_notice_CA(self, related_user, related_community, subtype, date=timezone.now):
        type = 'CA'
        if related_community is None:
            new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, subtype=subtype)
        else:
            new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, related_community=related_community, subtype=subtype)
        self.__create_notice_P(related_user, new_notice)

    def create_notice_B(self, related_user, description, date=timezone.now):
        type = 'B'
        new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, description=description)
        self.__create_notice_P(related_user, new_notice)

    def create_notice_C_AN(self, related_community, description, date=timezone.now):
        type = 'C_AN'
        new_notice = Notice.objects.create(date=date, type=type, related_community=related_community, description=description)
        self.__create_notice_C(related_community, new_notice)

    def create_notice_C_AP(self, related_user, related_community, subtype, date=timezone.now):
        type = 'C_AP'
        new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, related_community=related_community, subtype=subtype)
        self.__create_notice_C_A(related_community, new_notice)

    def create_notice_C_AA(self, related_user, related_community, description, date=timezone.now):
        type = 'C_AA'
        new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, related_community=related_community, description=description)
        self.__create_notice_C_A(related_community, new_notice)

    def create_notice_C_D(self, related_community, description, date=timezone.now):
        type = 'C_D'
        new_notice = Notice.objects.create(date=date, type=type, related_community=related_community, description=description)
        self.__create_notice_C(related_community, new_notice)

    def create_notice_S_CA(self, related_user, description, date=timezone.now):
        type = 'S_CA'
        new_notice = Notice.objects.create(date=date, type=type, related_user=related_user, description=description)
        self.__create_notice_S_CA(new_notice)
