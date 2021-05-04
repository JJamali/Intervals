import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from ..auth_testcase import AuthenticateTestCase
from django.test.client import MULTIPART_CONTENT

User = get_user_model()


# TODO: add tests for invalid settings
class TestSettings(AuthenticateTestCase):
    def test_get_settings(self):
        id = self.get_id('testuser')
        response = self.client.get(reverse('settings', kwargs={'id': id}))
        self.assertEqual(200, response.status_code)
        expected = {
            'current_level': 0,
            'playback_speed': 'N',
            'note_order': 'O',
        }
        self.assertDictEqual(expected, response.data)

    # PUT tests

    def test_put_complete_settings(self):
        """Put a new settings object with all fields"""
        self.login('testuser', '1')
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.put(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                   content_type=MULTIPART_CONTENT)
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('settings', kwargs={'id': id}))
        self.assertDictEqual(new_settings, response.data)

    def test_put_incomplete_settings(self):
        """Settings objects that are missing fields should be rejected"""
        self.login('testuser', '1')
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
        }
        response = self.client.put(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                   content_type=MULTIPART_CONTENT)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put_settings_unauthenticated(self):
        """Trying to update settings without authentication via PUT"""
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.put(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                   content_type=MULTIPART_CONTENT)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_settings_wrong_authorization(self):
        """Trying to update settings as wrong user"""
        self.login('testuser2', '2')
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.put(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                   content_type=MULTIPART_CONTENT)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    # PATCH tests

    def test_patch_complete_settings(self):
        """Put a new settings object with all fields"""
        self.login('testuser', '1')
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.patch(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                     content_type=MULTIPART_CONTENT)
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('settings', kwargs={'id': id}))
        self.assertDictEqual(new_settings, response.data)

    def test_patch_incomplete_settings(self):
        """Settings objects that are missing fields should be rejected"""
        self.login('testuser', '1')
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
        }
        response = self.client.patch(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                     content_type=MULTIPART_CONTENT)
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('settings', kwargs={'id': id}))
        self.assertDictEqual(dict(response.data, **new_settings), response.data)

    def test_patch_settings_unauthenticated(self):
        """Trying to update settings without authentication via PATCH"""
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.patch(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                     content_type=MULTIPART_CONTENT)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_patch_settings_wrong_authorization(self):
        """Trying to update settings as wrong user"""
        self.login('testuser2', '2')
        id = self.get_id('testuser')
        new_settings = {
            'current_level': 1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.patch(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                     content_type=MULTIPART_CONTENT)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def change_settings(self, username, password, new_settings):
        self.login(username, password)
        id = self.get_id(username)

        return self.client.patch(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                 content_type=MULTIPART_CONTENT)

    def test_change_current_level(self):
        new_settings = {'current_level': 1}
        self.change_settings('testuser', '1', new_settings)
        user = User.objects.get(username='testuser')
        self.assertEqual(1, user.profile.current_level)

    def test_change_speed(self):
        new_settings = {'playback_speed': 'S'}
        self.change_settings('testuser', '1', new_settings)
        user = User.objects.get(username='testuser')
        self.assertEqual('S', user.profile.playback_speed)

    def test_change_note_order(self):
        new_settings = {'note_order': 'R'}
        self.change_settings('testuser', '1', new_settings)
        user = User.objects.get(username='testuser')
        self.assertEqual('R', user.profile.note_order)

    # Test changing settings to invalid values
    def test_change_current_level_to_large_value(self):
        """Current level cannot be changed above the user's level."""
        user = User.objects.get(username='testuser')
        old = user.profile.current_level

        new_settings = {'current_level': user.profile.level + 1}

        response = self.change_settings('testuser', '1', new_settings)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        user.refresh_from_db()
        self.assertEqual(old, user.profile.current_level)

    def test_change_current_level_to_negative_value(self):
        """Current level cannot be set to a negative value."""
        user = User.objects.get(username='testuser')
        old = user.profile.current_level

        new_settings = {'current_level': -1}

        response = self.change_settings('testuser', '1', new_settings)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        user.refresh_from_db()
        self.assertEqual(old, user.profile.current_level)

    def test_change_speed_to_invalid_value(self):
        user = User.objects.get(username='testuser')
        old = user.profile.playback_speed

        new_settings = {'playback_speed': 'Z'}

        response = self.change_settings('testuser', '1', new_settings)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        user.refresh_from_db()
        self.assertEqual(old, user.profile.playback_speed)

    def test_change_note_order_to_invalid_value(self):
        user = User.objects.get(username='testuser')
        old = user.profile.note_order

        new_settings = {'note_order': 'Z'}

        response = self.change_settings('testuser', '1', new_settings)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        user.refresh_from_db()
        self.assertEqual(old, user.profile.note_order)

    def test_put_invalid_settings(self):
        self.login('testuser', '1')
        id = self.get_id('testuser')
        old = self.client.get(reverse('settings', kwargs={'id': id})).data

        new_settings = {
            'current_level': -1,
            'playback_speed': 'F',
            'note_order': 'R',
        }
        response = self.client.put(reverse('settings', kwargs={'id': id}), data=json.dumps(new_settings),
                                   content_type=MULTIPART_CONTENT)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response = self.client.get(reverse('settings', kwargs={'id': id}))
        self.assertDictEqual(old, response.data)
