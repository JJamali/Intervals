from django.test import TestCase
from django.contrib.auth import get_user_model
from intervalsApp.models import IntervalsProfile


class UserTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='first', password='num1')

    def test_user_creation_makes_profiles(self):
        """When a user is created an intervals profile should be made too"""
        User = get_user_model()
        first = User.objects.get(username='first')

        self.assertIsInstance(first.profile, IntervalsProfile)

