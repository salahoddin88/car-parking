from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token')
SIGNUP_URL = reverse('user:signup')


def create_user(**params):
    """ create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """ Test the public features of the user API """

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """ Test generate token for valid credentials """
        user_details = {
            'username': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'Name',
            'password': 'test-user-password123'
        }
        create_user(**user_details)
        payload = {
            'username': user_details['username'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentails(self):
        """ Test return error if credenatials are invalid """
        create_user(username='test@example.com', password="goodpass")
        payload = {
            'username': 'test@example.com',
            'password': 'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test posting a blank password return an error """
        payload = {
            'username': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SignupAPIViewTestCase(TestCase):
    """ Test the signup of the user API """

    def setUp(self):
        self.client = APIClient()

    def test_signup_valid_email_username(self):
        """ Test valid username as email """

        url = SIGNUP_URL
        payload = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_signup_valid_phone_username(self):
        """ Test valid username as phone """

        url = SIGNUP_URL
        payload = {
            'first_name': 'test',
            'last_name': 'user',
            'username': '9876543210',
            'password': 'password123',
            'password2': 'password123',
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_signup_invalid_username(self):
        """ Test invalid username as email """

        url = SIGNUP_URL
        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password': 'password123',
            'password2': 'password123',
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_signup_invalid_phone(self):
        """ Test invalid username as phone """

        url = SIGNUP_URL
        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': '12345678',
            'password': 'password123',
            'password2': 'password123',
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)
