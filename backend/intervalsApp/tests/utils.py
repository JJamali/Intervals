from rest_framework.test import APIClient
from django.urls import reverse


def get_access_token(username, password):

    response = APIClient().post(reverse('token_obtain_pair'), {'username': username, 'password': password})
    return response.data['access']


def get_auth_client(username, password):
    token = get_access_token(username, password)

    client = APIClient()
    # Adds Authorization: header
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return client
