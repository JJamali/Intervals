import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import MULTIPART_CONTENT
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


class GuestAuthTests(AuthenticateTestCase):
    def test_create_guest(self):
        # make sure no guests exists initially
        guests = list(User.objects.filter(is_guest=True))
        self.assertEqual(0, len(guests))
        # create a new guest
        response = self.client.post(reverse('login_guest'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # check that a guest was created
        guests = list(User.objects.filter(is_guest=True))
        self.assertEqual(1, len(guests))

    def test_guest_username(self):
        """Guests should have the 'Guest' username in API responses."""
        # login as a new guest
        response = self.client.post(reverse('login_guest'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        _id = self.client.get(reverse('current_user')).data['id']
        response = self.client.get(reverse('user-detail', kwargs={'id': _id}))
        self.assertEqual('Guest', response.data['username'])

    def test_convert_guest_to_user(self):
        """Creating a user while a guest account is active should
        convert the guest to a regular user."""

        # create a new guest
        response = self.client.post(reverse('login_guest'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # get guest user
        guest = User.objects.get(is_guest=True)

        # change guest setting
        _id = self.get_id(guest.username)
        new_settings = {'playback_speed': 'S'}
        self.client.patch(
            reverse('settings', kwargs={'id': _id}),
            data=json.dumps(new_settings),
            content_type=MULTIPART_CONTENT
        )

        # create new user account
        num_users = len(User.objects.all())
        response = self.client.post(reverse('user-list'), {'username': 'new_user', 'password': 'pass'})
        print(response.data)

        # check that the new user also has changed settings
        user = User.objects.get(username='new_user')
        self.assertEqual('S', user.profile.playback_speed)

        # check that the new user is not a guest
        self.assertFalse(user.is_guest)

        # check that the number of users did not increase
        self.assertEqual(num_users, len(User.objects.all()))

        # check that we are still logged in
        response = self.client.get(reverse('current_user'))
        self.assertEqual(self.get_id(user.username), response.data['id'])

