from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AuthenticateTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='1')
        User.objects.create_user(username='testuser2', password='2')

    def login(self, username, password):
        return self.client.post(reverse('login'), {'username': username, 'password': password})

    def logout(self):
        return self.client.post(reverse('logout'))

    def get_id(self, username):
        return User.objects.get(username=username).pk
