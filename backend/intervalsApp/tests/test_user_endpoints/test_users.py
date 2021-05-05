from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from ..auth_testcase import AuthenticateTestCase


User = get_user_model()


class TestUserList(AuthenticateTestCase):
    def test_user_list(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user1 = {'id': User.objects.get(username='testuser').pk, 'username': 'testuser'}
        user2 = {'id': User.objects.get(username='testuser2').pk, 'username': 'testuser2'}
        self.assertEqual(2, len(response.data))
        self.assertIn(user1, response.data)
        self.assertIn(user2, response.data)


class TestUserCreation(AuthenticateTestCase):
    def test_user_create(self):
        response = self.client.post(reverse('user-list'), {'username': 'new', 'password': '3'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response = self.login('new', '3')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Ensure logged in
        response = self.client.get(reverse('current_user'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_create_missing_username(self):
        response = self.client.post(reverse('user-list'), {'password': '3'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_create_missing_password(self):
        response = self.client.post(reverse('user-list'), {'username': 'new'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_create_when_logged_in(self):
        self.login('testuser', '1')
        self.test_user_create()

    def test_user_create_already_exists(self):
        response = self.client.post(reverse('user-list'), {'username': 'new', 'password': '3'})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        response = self.client.post(reverse('user-list'), {'username': 'new', 'password': '3'})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class TestUserData(AuthenticateTestCase):
    def test_get_user_data_without_authentication(self):
        """Tests that a get request from the current_user endpoint return the correct data.

        Checks for 200 response and all model fields."""
        id = self.get_id('testuser')
        response = self.client.get(reverse('user-detail', kwargs={'id': id}))
        self.assertEqual(200, response.status_code)

        expected_user = {'username': 'testuser',
                         'stats': {'level': 0,
                                   'recent': [{'level': 0,
                                               'total_correct': 0,
                                               'total_completed': 0,
                                               'recent_results': []
                                               }]
                                   },
                         'settings': {
                             'current_level': 0,
                             'playback_speed': 'N',
                             'note_order': 'O', }
                         }

        user = response.data

        self.maxDiff = None
        self.assertDictEqual(expected_user, user)
