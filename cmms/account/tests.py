from rest_framework.test import APITestCase
from .models import User


class LoginAndLogoutTests(APITestCase):
    def setUp(self):
        User.objects.create(gid="test", student_id="test", password="test")

    def test_traditional_login(self):
        # unfinished
        url = '/api/auth/login/'
        data = {'username': 'test', 'password': 'test'}

        response = self.client.post(url, data)
        print(response.content)
