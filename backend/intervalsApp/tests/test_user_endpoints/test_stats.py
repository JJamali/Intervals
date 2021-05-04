from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from ..auth_testcase import AuthenticateTestCase

User = get_user_model()


class TestStats(AuthenticateTestCase):
    def test_get_stats(self):
        id = self.get_id('testuser')
        response = self.client.get(reverse('stats', kwargs={'id': id}))
        self.assertEqual(200, response.status_code)
        expected = {'level': 0,
                    'recent': [{'level': 0,
                                'total_correct': 0,
                                'total_completed': 0,
                                'recent_results': []
                                }]
                    }
        self.assertDictEqual(expected, response.data)

    def test_cannot_modify_stats(self):
        """Stats aren't allowed to be edited"""
        self.login('testuser', '1')
        id = self.get_id('testuser')
        response = self.client.post(reverse('stats', kwargs={'id': id}))
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = self.client.put(reverse('stats', kwargs={'id': id}))
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = self.client.patch(reverse('stats', kwargs={'id': id}))
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = self.client.delete(reverse('stats', kwargs={'id': id}))
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
