from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class LoginAndLogoutTests(APITestCase):
    def setUp(self):
        User.objects.create_user(gid="testgid", student_id="teststuid", password="test")

    def test_traditional_login(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'teststuid', 'password': 'test'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["new"], True)

    def test_failed_traditional_login(self):
        url = '/api/auth/traditional_login'
        data = {'username': 'teststuid', 'password': '2333'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Sadly, CAS Login may be too hard to test.
