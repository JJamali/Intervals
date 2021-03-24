from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TokenObtainPairTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def test_login_user(self):
        """Test the regular login process that generates a token"""
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': '123'})
        self.assertEqual(response.status_code, 200)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        # We should also get the user data for convenience
        self.assertIn('user', response.data)

    def test_login_user_invalid_credentials(self):
        """Invalid login credentials should fail"""
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'username': 'testuser', 'password': 'wrong password'})
        # Expect a 401 (unauthorized) response
        self.assertEqual(response.status_code, 401)


class TokenRefreshTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', password='123')

    def test_refresh_token(self):
        """Check that the refresh endpoint works with a valid token"""
        refresh = self.client.post(reverse('token_obtain_pair'),
                                   {'username': 'testuser', 'password': '123'}).data['refresh']
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_invalid_refresh_token(self):
        """Check for a 401 response with an invalid token"""
        response = self.client.post(reverse('token_refresh'), {'refresh': 'invalid refresh'})
        self.assertEqual(response.status_code, 401)
