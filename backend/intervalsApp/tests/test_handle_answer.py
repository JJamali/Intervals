from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.apps import apps
from intervalsApp.models import RecentResults


class TestLevelUp(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def authenticate(self):
        self.client.post(reverse('login'), {'username': 'testuser', 'password': '123'})

    def send_correct_answer(self, username):
        User = get_user_model()
        user = User.objects.get(username=username)

        self.client.get(reverse('question'))
        correct_answer = user.profile.question.correct_answer
        self.client.post(reverse('answer_check'), {'guess': correct_answer}, format='json')

    def send_incorrect_answer(self, username):
        User = get_user_model()
        user = User.objects.get(username=username)

        self.client.get(reverse('question'))
        correct_answer = user.profile.question.correct_answer
        incorrect_answer = correct_answer + "to make this wrong, I am added"

        self.client.post(reverse('answer_check'), {'guess': incorrect_answer}, format='json')

    def test_level_up(self):
        self.authenticate()

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_correct_answer('testuser')

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level = user.profile.level

        self.assertEqual(level, 1)
        self.assertEqual(user.profile.current_level, 1)

    def test_not_level_up(self):
        self.authenticate()

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE - 1):
            self.send_correct_answer('testuser')

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level = user.profile.level

        self.assertEqual(level, 0)

    def test_20_incorrect(self):
        self.authenticate()

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_incorrect_answer('testuser')

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level = user.profile.level

        self.assertEqual(level, 0)

    # Test that user does not exceed max level
    def test_max_level(self):
        self.authenticate()

        User = get_user_model()
        user = User.objects.get(username='testuser')

        user.profile.level = apps.get_app_config('intervalsApp').TOTAL_LEVELS

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE + 10):
            self.send_correct_answer('testuser')

        level = user.profile.level

        self.assertEqual(level, apps.get_app_config('intervalsApp').TOTAL_LEVELS)

    # Test to see if current_level.recent_results is saved properly
    def test_current_level_recent_results(self):
        self.authenticate()

        User = get_user_model()
        user = User.objects.get(username='testuser')

        current_user = user.profile
        recent_results = current_user.recent_results_at_level(current_user.current_level)
        self.send_correct_answer('testuser')

        current_user.current_level = 1

        second_recent_results = current_user.recent_results_at_level(current_user.current_level)
        self.assertNotEqual(recent_results, second_recent_results)

    def test_level_up_creates_recent_results(self):
        """A level up should create an empty recent results object
        for the new level"""
        self.authenticate()

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_correct_answer('testuser')

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level_one_result = RecentResults.objects.get(profile=user.profile, level=1)
        self.assertListEqual(level_one_result.recent_results, [])
