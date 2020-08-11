from django.contrib.auth.models import AbstractUser
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from .models import Community


class CommunitiesTests(APITestCase):
    def create_community(self, user: User, name: str, profile: str = '', valid: bool = True) -> Community:
        c: Community = Community.objects.create(creator=user, owner=user, name=name,
                                                profile=profile, valid=valid)
        c.admins.add(user)
        c.members.add(user, through_defaults={'valid': True})  # type: ignore
        return c

    def login_as_user(self, user: AbstractUser):
        self.client.force_login(user)

    def login_sysadmin(self):
        self.client.login(username='sysadmin', password='sysadmin')

    def setUp(self):
        self.user1 = User.objects.create_user(gid="testgid", student_id="teststuid", password="test",
                                              profile="testprofile", nick_name="user1", real_name="user11")
        self.user2 = User.objects.create_user(gid="gid2", student_id="PB23333333", password="test2",
                                              nick_name="myname", real_name="myname2")
        self.user3 = User.objects.create_superuser(gid="gid3", student_id="sysadmin", password="sysadmin",
                                                   nick_name="sysadmin", real_name="sysadmin")
        self.club1 = self.create_community(user=self.user1, name='club1', profile='thisisclub1', valid=True)
        self.club2 = self.create_community(user=self.user2, name='club2', profile='thisisclub2', valid=True)
        self.club3 = self.create_community(user=self.user3, name='club3', profile='thisisclub3', valid=False)

    def test_list_communities(self):
        url = '/api/community/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'club1')
        self.assertEqual(response.data[0]['profile'], 'thisisclub1')

    def test_retrieve_community(self):
        url = f'/api/community/{self.club1.id}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'club1')
        self.assertEqual(response.data['join_status'], '')

        self.login_as_user(self.user2)

        url = f'/api/community/{self.club1.id}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['join_status'], '未加入')

        url = f'/api/community/{self.club2.id}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['join_status'], '已加入')

        url = f'/api/community/{self.club3.id}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()

    def test_update_community(self):
        url = f'/api/community/{self.club2.id}'
        self.login_as_user(self.user2)

        response = self.client.patch(url, {
            'profile': 'fjwtql!!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile'], 'fjwtql!!')
        response = self.client.patch(url, {
            'profile': 'thisisclub2'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_destroy_community(self):
        url = f'/api/community/{self.club2.id}'
        self.login_as_user(self.user2)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.club2 = self.create_community(user=self.user2, name='club2', profile='thisisclub2', valid=True)
        self.client.logout()

    def test_create_and_audit_community(self):
        url = '/api/community/'
        self.login_as_user(self.user2)

        response = self.client.post(url, {
            'name': 'ZJX Club',
            'profile': 'zjxtql'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        id = response.data['id']
        self.client.logout()

        self.login_sysadmin()
        url = '/api/community/audit/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = f'/api/community/audit/{id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'ZJX Club')

        response = self.client.put(url, {
            'valid': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

        self.login_as_user(self.user2)
        url = '/api/community/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        url = f'/api/community/{id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_join(self):
        url = f'/api/community/{self.club1.id}/join'
        self.login_as_user(self.user2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'member': False,
            'valid': False,
        })
        response = self.client.post(url, {
            'join': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'member': True,
            'valid': False
        })
        self.client.logout()
        self.login_as_user(self.user1)
        url2 = f'/api/community/{self.club1.id}/audit'
        response = self.client.get(url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        url2 = f'/api/community/{self.club1.id}/audit/{self.user2.id}/allow'
        response = self.client.post(url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

        self.login_as_user(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'member': True,
            'valid': True,
        })
        response = self.client.post(url, {
            'join': False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'member': False,
            'valid': False
        })

    def test_invite(self):
        url = f'/api/community/{self.club2.id}/invite'
        self.login_as_user(self.user2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['non_members']), 2)
        url = f'/api/community/{self.club2.id}/invite/{self.user1.id}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

        url = f'/api/community/invitation/'
        self.login_as_user(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        invitation_id = response.data[0]['id']

        url = f'/api/community/invitation/{invitation_id}/accept/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = f'/api/community/{self.club2.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['members']), 2)

        url = f'/api/community/{self.club2.id}/join'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'member': True,
            'valid': True
        })
        response = self.client.post(url, {
            'join': False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'member': False,
            'valid': False
        })
        self.client.logout()

    def test_checklist(self):
        url = f'/api/community/{self.club1.id}/checklist'
        self.login_as_user(self.user1)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': []
        })
        response = self.client.post(url + '/create', {
            'contents': 'fjwtql'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': [['fjwtql', False]]
        })
        response = self.client.post(url + '/create', {
            'contents': 'zjxtql'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': [['fjwtql', False], ['zjxtql', False]]
        })
        response = self.client.post(url + '/swap', {
            'index_from': 0,
            'index_to': 1
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': [['zjxtql', False], ['fjwtql', False]]
        })
        response = self.client.post(url + '/set', {
            'index': 0,
            'done': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': [['zjxtql', True], ['fjwtql', False]]
        })
        response = self.client.post(url + '/remove', {
            'index': 0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': [['fjwtql', False]]
        })
        response = self.client.post(url + '/remove', {
            'index': 0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'checklist': []
        })
        self.client.logout()

    def test_set_admin_and_transfer(self):
        url = f'/api/community/{self.club1.id}/join'
        self.login_as_user(self.user2)
        response = self.client.post(url, {
            'join': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        self.login_as_user(self.user1)
        url = f'/api/community/{self.club1.id}/audit/{self.user2.id}/allow'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = f'/api/community/{self.club1.id}/members/{self.user2.id}/admin/set'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = f'/api/community/{self.club1.id}/transfer'

        response = self.client.put(url, {
            'owner': self.user2.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'owner': self.user2.id
        })
        response = self.client.put(url, {
            'owner': self.user1.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        self.login_as_user(self.user2)
        response = self.client.put(url, {
            'owner': self.user1.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'owner': self.user1.id
        })
        self.client.logout()
        self.login_as_user(self.user1)
        url = f'/api/community/{self.club1.id}/members/{self.user2.id}/admin/unset'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = f'/api/community/{self.club1.id}/members/{self.user2.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()
