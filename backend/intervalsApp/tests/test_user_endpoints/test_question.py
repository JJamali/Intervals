from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from ..auth_testcase import AuthenticateTestCase

User = get_user_model()


class TestQuestion(AuthenticateTestCase):
    def test_get_question_does_not_exist(self):
        id = self.get_id('testuser')
        response = self.client.get(reverse('question', kwargs={'id': id}))
        self.assertEqual(404, response.status_code)

    def test_create_question_not_authenticated(self):
        id = self.get_id('testuser')
        response = self.client.post(reverse('question', kwargs={'id': id}))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_question_wrong_authentication(self):
        self.login('testuser2', '2')
        id = self.get_id('testuser')
        response = self.client.post(reverse('question', kwargs={'id': id}))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_question(self):
        self.login('testuser', '1')
        id = self.get_id('testuser')
        response = self.client.post(reverse('question', kwargs={'id': id}))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        question = response.data
        self.assertIn('question_text', question)
        self.assertIn('first_note', question)
        self.assertIn('second_note', question)
        self.assertIn('answers', question)
        self.assertNotIn('correct_answer', question)

    def test_get_question_exists(self):
        self.login('testuser', '1')
        id = self.get_id('testuser')
        self.client.post(reverse('question', kwargs={'id': id}))
        self.logout()

        response = self.client.get(reverse('question', kwargs={'id': id}))
        self.assertEqual(200, response.status_code)

        question = response.data
        self.assertIn('question_text', question)
        self.assertIn('first_note', question)
        self.assertIn('second_note', question)
        self.assertIn('answers', question)
        self.assertNotIn('correct_answer', question)
