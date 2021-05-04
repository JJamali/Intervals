from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from ..auth_testcase import AuthenticateTestCase
from django.apps import apps
from intervalsApp.models import RecentResults

User = get_user_model()


class TestAnswer(AuthenticateTestCase):
    def create_question(self, username):
        id = self.get_id(username)
        response = self.client.post(reverse('question', kwargs={'id': id}))
        return response

    def test_answer_not_authenticated(self):
        id = self.get_id('testuser')
        response = self.client.post(reverse('answer', kwargs={'id': id}))
        self.assertEqual(403, response.status_code)

    def test_answer_wrong_authentication(self):
        self.login('testuser2', '2')
        id = self.get_id('testuser')
        response = self.client.post(reverse('answer', kwargs={'id': id}))
        self.assertEqual(403, response.status_code)

    def test_answer_without_question(self):
        self.login('testuser', '1')
        id = self.get_id('testuser')
        response = self.client.post(reverse('answer', kwargs={'id': id}), data={'guess': ''})
        self.assertEqual(404, response.status_code)

    def test_answer_missing_guess(self):
        self.login('testuser', '1')
        id = self.get_id('testuser')
        response = self.client.post(reverse('answer', kwargs={'id': id}))
        self.assertEqual(400, response.status_code)

    def test_check_correct_answer(self):
        self.login('testuser', '1')

        self.create_question('testuser')

        # Get correct answer from user model
        user = User.objects.get(username='testuser')
        correct_answer = user.profile.question.correct_answer

        id = self.get_id('testuser')
        response = self.client.post(reverse('answer', kwargs={'id': id}), data={'guess': correct_answer})
        self.assertEqual(200, response.status_code)
        expected = {'correct': True, 'correct_answer': correct_answer}
        self.assertDictEqual(expected, response.data)

    def test_check_incorrect_answer(self):
        self.login('testuser', '1')

        self.create_question('testuser')

        # Get correct answer from user model
        user = User.objects.get(username='testuser')
        correct_answer = user.profile.question.correct_answer
        incorrect_answer = correct_answer + "to make this wrong, I am added"

        id = self.get_id('testuser')
        response = self.client.post(reverse('answer', kwargs={'id': id}), data={'guess': incorrect_answer})
        self.assertEqual(200, response.status_code)
        expected = {'correct': False, 'correct_answer': correct_answer}
        self.assertDictEqual(expected, response.data)


class TestLevelUp(AuthenticateTestCase):
    """Tests leveling up through answering questions."""
    def send_correct_answer(self, username):
        id = self.get_id(username)
        self.client.post(reverse('question', kwargs={'id': id}))

        user = User.objects.get(username=username)
        correct_answer = user.profile.question.correct_answer
        self.client.post(reverse('answer', kwargs={'id': id}), data={'guess': correct_answer})

    def send_incorrect_answer(self, username):
        id = self.get_id(username)
        self.client.post(reverse('question', kwargs={'id': id}))

        user = User.objects.get(username=username)
        correct_answer = user.profile.question.correct_answer
        incorrect_answer = correct_answer + "to make this wrong, I am added"
        self.client.post(reverse('answer', kwargs={'id': id}), data={'guess': incorrect_answer})

    def test_level_up(self):
        """Test that user levels up with minimum amount of answers, all of which are correct."""
        self.login('testuser', '1')

        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_correct_answer('testuser')

        user = User.objects.get(username='testuser')
        level = user.profile.level
        self.assertEqual(level, 1)
        self.assertEqual(user.profile.current_level, 1)

    # TODO: fix this test cause it's borked
    def test_level_up_with_minimum_score(self):
        """Test that user levels up with minimum amount of answers, with some incorrect answers."""
        self.login('testuser', '1')

        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE - int(
                apps.get_app_config('intervalsApp').SCORE_RANGE / 20)):
            self.send_correct_answer('testuser')

        for _ in range(int(apps.get_app_config('intervalsApp').SCORE_RANGE / 20)):
            self.send_correct_answer('testuser')

        user = User.objects.get(username='testuser')
        level = user.profile.level
        self.assertEqual(level, 1)
        self.assertEqual(user.profile.current_level, 1)

    def test_not_level_up(self):
        """Test that user does not level up before answering minimum amount of questions."""
        self.login('testuser', '1')

        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE - 1):
            self.send_correct_answer('testuser')

        user = User.objects.get(username='testuser')
        level = user.profile.level
        self.assertEqual(level, 0)

    def test_20_incorrect(self):
        """Test that user does not level up with incorrect answers."""
        self.login('testuser', '1')

        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_incorrect_answer('testuser')

        user = User.objects.get(username='testuser')
        level = user.profile.level
        self.assertEqual(level, 0)

    def test_max_level(self):
        """Test that user does not exceed max level."""
        self.login('testuser', '1')

        user = User.objects.get(username='testuser')

        # set the user's level to the maximum level
        user.profile.level = apps.get_app_config('intervalsApp').TOTAL_LEVELS

        # this should level up the user if they aren't at the max level
        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE + 10):
            self.send_correct_answer('testuser')

        # check that they are still at the max level (and haven't leveled up by extension)
        level = user.profile.level
        self.assertEqual(level, apps.get_app_config('intervalsApp').TOTAL_LEVELS)

    def test_current_level_recent_results(self):
        """Test to see if current_level.recent_results is saved properly."""
        self.login('testuser', '1')

        user = User.objects.get(username='testuser')

        profile = user.profile
        recent_results = profile.recent_results_at_level(profile.current_level)
        self.send_correct_answer('testuser')

        profile.current_level = 1

        second_recent_results = profile.recent_results_at_level(profile.current_level)
        self.assertNotEqual(recent_results, second_recent_results)

    def test_level_up_on_previous_level(self):
        """Test that user does not level up when visiting previous levels."""
        self.login('testuser', '1')

        user = User.objects.get(username='testuser')

        profile = user.profile
        profile.level = 4
        profile.current_level = 2
        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE + 10):
            self.send_correct_answer('testuser')

        self.assertEqual(profile.current_level, 2)

    def test_level_up_creates_recent_results(self):
        """A level up should create an empty recent results object for the new level."""
        self.login('testuser', '1')

        for _ in range(apps.get_app_config('intervalsApp').SCORE_RANGE):
            self.send_correct_answer('testuser')

        user = User.objects.get(username='testuser')

        level_one_result = RecentResults.objects.get(profile=user.profile, level=1)
        self.assertListEqual(level_one_result.recent_results, [])
