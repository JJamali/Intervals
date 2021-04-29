from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class CurrentUserTests(TestCase):
    """Tests for intervals api."""
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def authenticate(self, username, password):
        self.client.post(reverse('login'), {'username': username, 'password': password})

    def get_access_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_get_current_user(self):
        """Tests that a get request from the current_user endpoint return the correct data.

        Checks for 200 response and all model fields."""
        self.authenticate('testuser', '123')

        response = self.client.get(reverse('current_user'))
        self.assertEqual(200, response.status_code)

        expected_user = {'username': 'testuser',
                         'profile': {'level': 0,
                                     'current_level': 0,
                                     'playback_speed': 'N',
                                     'note_order': 'O',
                                     'recent': [{'level': 0,
                                                 'total_correct': 0,
                                                 'total_completed': 0,
                                                 'recent_results': []
                                                 }]
                                     }
                         }

        user = response.data

        self.maxDiff = None
        self.assertDictEqual(expected_user, user)

    def test_get_current_user_invalid_credentials(self):
        self.authenticate('testuser', 'invalid')
        response = self.client.get(reverse('current_user'))
        self.assertEqual(401, response.status_code)

    def test_settings_change(self):
        self.authenticate('testuser', '123')
        self.client.post(reverse('update_settings'), {'playback_speed': 'S'})

        User = get_user_model()
        user = User.objects.get(username='testuser')
        self.assertEqual('S', user.profile.playback_speed)


class QuestionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def authenticate(self, username, password):
        self.client.post(reverse('login'), {'username': username, 'password': password})

    def get_access_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_get_question(self):
        self.authenticate('testuser', '123')
        response = self.client.get(reverse('question'))
        self.assertEqual(201, response.status_code)

        question = response.data
        self.assertIn('question_text', question)
        self.assertIn('first_note', question)
        self.assertIn('second_note', question)
        self.assertIn('answers', question)
        self.assertNotIn('correct_answer', question)
