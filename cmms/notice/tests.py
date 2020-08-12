from rest_framework.test import APITestCase

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .models import Notice, NoticeBox
from .utils import NoticeManager
from .serializers import NoticeSerializer

from account.models import User

from communities.models import Community

from activity.models import Activity


class NoticeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(gid="test0",
                                             student_id="test0",
                                             password="test0",
                                             nick_name="user",
                                             real_name="user")
        self.another_user = User.objects.create_user(gid="test1",
                                                     student_id="test1",
                                                     password="test1",
                                                     nick_name="another_user",
                                                     real_name="another_user")
        self.member = User.objects.create_user(gid="test2",
                                               student_id="test2",
                                               password="test2",
                                               nick_name="member",
                                               real_name="member")
        self.community_admin = User.objects.create_user(
            gid="test3",
            student_id="test3",
            password="test3",
            nick_name="community_admin",
            real_name="community_admin")
        self.system_admin = User.objects.create_superuser(
            gid="test4",
            student_id="test4",
            password="test4",
            nick_name="system_admin",
            real_name="system_admin")
        self.community = Community.objects.create(creator=self.community_admin,
                                                  owner=self.community_admin,
                                                  name="Test Community",
                                                  valid=True)
        self.community.admins.add(self.community_admin)
        self.community.members.add(self.community_admin,
                                   through_defaults={'valid': True})
        self.community.members.add(self.member,
                                   through_defaults={'valid': True})
        self.time = timezone.now()
        self.activity = Activity.objects.create(
            related_community=self.community,
            start_time=self.time,
            end_time=self.time)

    def login_as_user(self, user: User):
        self.client.force_login(user)

    def login_sysadmin(self):
        self.client.login(username='test4', password='test4')

    def check(self, user: User, notice: Notice) -> bool:
        self.login_as_user(user)
        serialized_data = NoticeSerializer(notice).data
        url = '/api/notice/'
        boxResponse = self.client.get(url).data

        for box in boxResponse:  # type: ignore
            noticeResponse = self.client.post(url, {'pk': int(box['pk'])}).data

            if noticeResponse == serialized_data:
                return True

        return False

    def syscheck(self, notice: Notice) -> bool:
        self.login_sysadmin()
        serialized_data = NoticeSerializer(notice).data
        url = '/api/notice/'
        boxResponse = self.client.get(url).data

        for box in boxResponse:  # type: ignore
            noticeResponse = self.client.post(url, {'pk': int(box['pk'])}).data

            if noticeResponse == serialized_data:
                return True

        return False

    def testPCDistribution(self):
        # PC 通知只有当事人能查看，其他人不能查看

        notice = NoticeManager.create_notice_PC(self.user, self.community, 0)

        self.assertEqual(self.check(self.user, notice), True)
        self.assertEqual(self.check(self.another_user, notice), False)

    def testARDistribution(self):
        pass

    def testCADistribution(self):
        # CA 通知只有当事人能查看，其他人不能查看

        notice = NoticeManager.create_notice_CA(self.user, self.community, 0)

        self.assertEqual(self.check(self.user, notice), True)
        self.assertEqual(self.check(self.another_user, notice), False)

    def testBDistribution(self):
        # B 通知只有当事人能查看，其他人不能查看

        notice = NoticeManager.create_notice_B(self.user)

        self.assertEqual(self.check(self.user, notice), True)
        self.assertEqual(self.check(self.another_user, notice), False)

    def testCANDistribution(self):
        # CAN 通知只有社团成员和社团管理员能查看，其他人不能查看

        notice = NoticeManager.create_notice_C_AN(self.activity, 0)

        self.assertEqual(self.check(self.user, notice), False)
        self.assertEqual(self.check(self.member, notice), True)
        self.assertEqual(self.check(self.community_admin, notice), True)

    def testCAPDistribution(self):
        # CAP 通知只有社团管理员能查看，其他人不能查看

        notice = NoticeManager.create_notice_C_AP(self.user, self.community, 0)

        self.assertEqual(self.check(self.user, notice), False)
        self.assertEqual(self.check(self.member, notice), False)
        self.assertEqual(self.check(self.community_admin, notice), True)

    def testCAADistribution(self):
        # CAA 通知只有社团管理员能查看，其他人不能查看

        notice = NoticeManager.create_notice_C_AA(self.user, self.community)

        self.assertEqual(self.check(self.user, notice), False)
        self.assertEqual(self.check(self.member, notice), False)
        self.assertEqual(self.check(self.community_admin, notice), True)

    def testCDDistribution(self):
        # CD 通知只有社团成员和社团管理员能查看，其他人不能查看

        notice = NoticeManager.create_notice_C_D(self.community)

        self.assertEqual(self.check(self.user, notice), False)
        self.assertEqual(self.check(self.member, notice), True)
        self.assertEqual(self.check(self.community_admin, notice), True)

    def testSCADistribution(self):
        # SCA 通知只有系统管理员能查看，其他人不能查看

        notice = NoticeManager.create_notice_S_CA(self.user)

        self.assertEqual(self.check(self.user, notice), False)
        self.assertEqual(self.syscheck(notice), True)
