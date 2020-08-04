from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class LoginAndLogoutTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(gid="testgid", student_id="teststuid",
                                              password="test", profile="testprofile")
        self.user2 = User.objects.create_user(gid="gid2", student_id="PB23333333",
                                              password="test2", nick_name="myname", phone="123")

    def test_traditional_login_new_user(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'teststuid', 'password': 'test'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_traditional_login_old_user(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'PB23333333', 'password': 'test2'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_failed_traditional_login(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'teststuid', 'password': '2333'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Sadly, CAS Login may be too hard to test.

    def test_get_all_users_info(self):
        url = '/api/users/public/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in response.data:
            if i["pk"] == 1:
                self.assertEqual(i["profile"], "testprofile")
            elif i["pk"] == 2:
                self.assertEqual(i["nick_name"], "myname")
            self.assertEqual(i.get("real_name"), None)  # not leaking private info

    def test_get_my_info(self):
        self.test_traditional_login_old_user()
        url = '/api/users/current'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "123")

        response = self.client.patch(url, {
            "phone": "4567"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "4567")

    def test_login_check(self):
        url = '/api/auth/check'

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'login': False,
            'new': None,
            'userid': None
        })

        self.test_traditional_login_old_user()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'login': True,
            'new': False,
            'userid': self.user2.id
        })
