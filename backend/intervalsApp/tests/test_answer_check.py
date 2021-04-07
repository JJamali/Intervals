from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


class AnswerCheckTests(TestCase):
    """Tests for answer check endpoint"""
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def test_check_correct_answer(self):
        token = self.get_access_token('testuser', '123')

        client = APIClient()
        # Adds Authorization: header
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        client.get(reverse('question'))

        User = get_user_model()
        user = User.objects.get(username='testuser')

        correct_answer = user.profile.question.correct_answer

        response = client.post(reverse('answer_check'), {'guess': correct_answer}, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.data['correct'])
        self.assertEqual(correct_answer, response.data['correct_answer'])

    def test_check_incorrect_answer(self):
        token = self.get_access_token('testuser', '123')

        client = APIClient()
        # Adds Authorization: header
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        client.get(reverse('question'))

        User = get_user_model()
        user = User.objects.get(username='testuser')

        correct_answer = user.profile.question.correct_answer
        incorrect_answer = correct_answer + "to make this wrong, I am added"

        response = client.post(reverse('answer_check'), {'guess': incorrect_answer}, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(False, response.data['correct'])
        self.assertEqual(correct_answer, response.data['correct_answer'])

    def get_access_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_invalid_data(self):
        token = self.get_access_token('testuser', '123')

        client = APIClient()
        # Adds Authorization: header
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'question': {'question': 'question prompt',
                             'answers': 'not a list',
                             'correct_answer': '1',
                             'first_note': '1',
                             'second_note': '2'},
                'guess': '2'}
        response = client.post(reverse('answer_check'), data, format='json')
        self.assertEqual(400, response.status_code)