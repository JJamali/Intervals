from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


class CurrentUserTests(TestCase):
    """Tests for intervals api"""
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def get_access_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_get_current_user(self):
        token = self.get_access_token('testuser', '123')

        client = APIClient()
        # Adds Authorization: header
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = client.get(reverse('current_user'))
        self.assertEqual(200, response.status_code)
        user = response.data
        self.assertEqual('testuser', user['username'])

    def test_get_current_user_invalid_token(self):
        client = APIClient()
        # Adds Authorization: header
        client.credentials(HTTP_AUTHORIZATION=f'Bearer invalid')

        response = client.get(reverse('current_user'))
        self.assertEqual(401, response.status_code)


class QuestionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def get_access_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_get_question(self):
        response = self.client.get(reverse('question'))
        self.assertEqual(201, response.status_code)

        question = response.data
        self.assertIn('question', question)
        self.assertIn('answers', question)
        self.assertIn('correct_answer', question)

