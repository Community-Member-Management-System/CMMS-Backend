from django.contrib.auth.models import AbstractUser
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from django.utils import timezone
from communities.models import Community
from .models import Activity
import datetime

# Create your tests here.
class ActivitiesTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(gid='gid1', student_id='sid1', password='passwd',
                                              profile='profile1', nick_name='stu1', real_name='name1')
        self.user2 = User.objects.create_user(gid='gid2', student_id='sid2', password='passwd',
                                              profile='profile2', nick_name='stu2', real_name='name2')
        self.user3 = User.objects.create_user(gid='gid3', student_id='sid3', password='passwd',
                                              profile='profile3', nick_name='stu3', real_name='name3')
        self.user4 = User.objects.create_user(gid='gid4', student_id='sid4', password='passwd',
                                              profile='profile4', nick_name='stu4', real_name='name4')
        self.community1 = Community.objects.create(creator=self.user1, owner=self.user1, name='com1',
                                                   profile='comprofile1', valid=True)
        self.community2 = Community.objects.create(creator=self.user2, owner=self.user2, name='com2',
                                                   profile='comprofile2', valid=True)
        self.community1.admins.add(self.user1)
        self.community2.admins.add(self.user2)
        self.community1.members.add(self.user1, through_defaults={'valid': True})
        self.community2.members.add(self.user2, through_defaults={'valid': True})
        self.community1.members.add(self.user3, through_defaults={'valid': True})
        self.community2.members.add(self.user4)
        now = timezone.datetime.now()
        self.activity1 = Activity.objects.create(related_community=self.community1, location='loc1',
                                                 title='title1', description='des1',
                                                 start_time=now - timezone.timedelta(minutes=60),
                                                 end_time=now + timezone.timedelta(minutes=60))
        self.activity2 = Activity.objects.create(related_community=self.community2, location='loc2',
                                                 title='title2', description='des2',
                                                 start_time=now - timezone.timedelta(minutes=60),
                                                 end_time=now - timezone.timedelta(minutes=30))
        self.activity3 = Activity.objects.create(related_community=self.community2, location='loc3',
                                                 title='title3', description='des3',
                                                 start_time=now + timezone.timedelta(minutes=30),
                                                 end_time=now + timezone.timedelta(minutes=60))

    def test_create_activity(self):
        url = '/api/activity/'

        response = self.client.post(url, {
            'related_community': self.community1.id,
            'location': 'loctest3',
            'title': 'titletest3',
            'description': 'destest3',
            'start_time': '2020-01-01T00:00:00+08:00',
            'end_time': '2020-01-01T01:00:00+08:00'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user3)
        response = self.client.post(url, {
            'related_community': self.community1.id,
            'location': 'loctest3',
            'title': 'titletest3',
            'description': 'destest3',
            'start_time': '2020-01-01T00:00:00+08:00',
            'end_time': '2020-01-01T01:00:00+08:00'
        })
        #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        response = self.client.post(url, {
            'related_community': self.community1.id,
            'location': 'loctest1',
            'title': 'titletest1',
            'description': 'destest1',
            'start_time': '2020-01-01T00:00:00+08:00',
            'end_time': '2020-01-01T01:00:00+08:00',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        response = self.client.get('/api/activity/')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'title1')
        self.assertEqual(response.data[1]['title'], 'title2')
        self.assertEqual(response.data[2]['title'], 'title3')
        self.assertEqual(response.data[0]['status'], '进行中')
        self.assertEqual(response.data[1]['status'], '已结束')
        self.assertEqual(response.data[2]['status'], '未开始')

        response = self.client.get(f'/api/activity/?community={self.community1.id}')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'title1')

        self.client.force_login(self.user2)
        response = self.client.get(f'/api/activity/?only_mine')
        self.assertEqual(len(response.data), 2)

    def test_token(self):
        response = self.client.get(f'/api/activity/{self.community1.id}/secret_key')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_login(self.user3)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_login(self.user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)