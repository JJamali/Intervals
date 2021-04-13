from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class CurrentUserTests(TestCase):
    """Tests for intervals api"""
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def authenticate(self, username, password):
        self.client.post(reverse('login'), {'username': username, 'password': password})

    def get_access_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_get_current_user(self):
        self.authenticate('testuser', '123')

        response = self.client.get(reverse('current_user'))
        self.assertEqual(200, response.status_code)
        user = response.data
        self.assertEqual('testuser', user['username'])

    def test_get_current_user_invalid_credentials(self):
        self.authenticate('testuser', 'invalid')
        response = self.client.get(reverse('current_user'))
        self.assertEqual(401, response.status_code)


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
