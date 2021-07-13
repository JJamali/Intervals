from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import timedelta
import time

from ..management.commands.clearguests import clear_guests


class ClearGuestTests(TestCase):
    def create_guest(self):
        self.client.post(reverse('login_guest'))

    def test_clear_guest(self):
        self.create_guest()
        self.assertEqual(1, len(get_user_model().objects.filter(is_guest=True)))

        num_deleted = clear_guests(timedelta(seconds=3))
        self.assertEqual(0, num_deleted)
        self.assertEqual(1, len(get_user_model().objects.filter(is_guest=True)))

        time.sleep(5)
        num_deleted = clear_guests(timedelta(seconds=3))
        self.assertEqual(1, num_deleted)
        self.assertEqual(0, len(get_user_model().objects.filter(is_guest=True)))
