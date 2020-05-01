from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class LoginAndLogoutTests(APITestCase):
    def setUp(self):
        User.objects.create_user(gid="test", student_id="test", password="test")

    def test_traditional_login(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'test', 'password': 'test'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_traditional_login(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'test', 'password': '2333'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Sadly, CAS Login may be too hard to test.
