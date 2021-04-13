from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


class LoginTests(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def authenticate(self, username, password):
        return self.client.post(reverse('login'), {'username': username, 'password': password})

    # Login section
    def test_login(self):
        response = self.authenticate('testuser', '123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_when_logged_in(self):
        self.authenticate('testuser', '123')
        response = self.authenticate('testuser', '123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Logout section
    def test_logout(self):
        self.authenticate('testuser', '123')

        self.client.post(reverse('logout'))
        response = self.client.post(reverse('current_user'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_when_not_logged_in(self):

        self.client.post(reverse('logout'))
        response = self.client.post(reverse('current_user'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
