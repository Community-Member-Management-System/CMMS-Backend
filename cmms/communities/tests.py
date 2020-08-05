from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from .models import Community


class CommunitiesTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(gid="testgid", student_id="teststuid", password="test",
                                              profile="testprofile", nick_name="user1", real_name="user11")
        self.user2 = User.objects.create_user(gid="gid2", student_id="PB23333333", password="test2",
                                              nick_name="myname", real_name="myname2")
        self.club1 = Community.objects.create(creator=self.user1, owner=self.user1, name='club1',
                                              profile='thisisclub1', valid=True)
        self.club2 = Community.objects.create(creator=self.user2, owner=self.user2, name='club2',
                                              profile='thisisclub2', valid=True)

    def test_list_community(self):
        url = '/api/community/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'club1')
        self.assertEqual(response.data[0]['profile'], 'thisisclub1')
