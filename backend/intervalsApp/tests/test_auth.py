from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .auth_testcase import AuthenticateTestCase

User = get_user_model()


class AuthTests(AuthenticateTestCase):
    # Login section
    def test_login(self):
        response = self.login('testuser', '1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_when_logged_in(self):
        self.login('testuser', '123')
        response = self.login('testuser', '1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Logout section
    def test_logout(self):
        self.login('testuser', '1')

        self.client.post(reverse('logout'))
        response = self.client.get(reverse('current_user'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_logout_when_not_logged_in(self):
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('current_user'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_current_user_logged_in(self):
        self.login('testuser', '1')
        response = self.client.get(reverse('current_user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username='testuser').pk, response.data['id'])

    def test_current_user_logged_out(self):
        response = self.client.get(reverse('current_user'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
