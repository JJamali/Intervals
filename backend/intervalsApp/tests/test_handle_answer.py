from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.apps import apps
from . import utils


class TestLevelUp(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def send_correct_answer(self, username, client):
        User = get_user_model()
        user = User.objects.get(username=username)

        client.get(reverse('question'))
        correct_answer = user.profile.question.correct_answer
        client.post(reverse('answer_check'), {'guess': correct_answer}, format='json')

    def send_incorrect_answer(self, username, client):
        User = get_user_model()
        user = User.objects.get(username=username)

        client.get(reverse('question'))
        correct_answer = user.profile.question.correct_answer
        incorrect_answer = correct_answer + "to make this wrong, I am added"

        client.post(reverse('answer_check'), {'guess': incorrect_answer}, format='json')

    def test_level_up(self):
        client = utils.get_auth_client('testuser', '123')

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_correct_answer('testuser', client)

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level = user.profile.level

        self.assertEqual(level, 1)

    def test_not_level_up(self):
        client = utils.get_auth_client('testuser', '123')

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE - 1):
            self.send_correct_answer('testuser', client)

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level = user.profile.level

        self.assertEqual(level, 0)

    def test_20_incorrect(self):
        client = utils.get_auth_client('testuser', '123')

        for x in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_incorrect_answer('testuser', client)

        User = get_user_model()
        user = User.objects.get(username='testuser')

        level = user.profile.level

        self.assertEqual(level, 0)
