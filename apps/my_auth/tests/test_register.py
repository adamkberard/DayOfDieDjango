from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.players.models import Player

from .checkers import AuthTesting
from .factories import DEFAULT_PASSWORD, PlayerFactory


class Test_Register_View(AuthTesting):

    def test_correct_register(self):
        """Testing a legitimate registration."""
        data = {'email': 'testEmail@gmail.com', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)
        user = Player.objects.get(email=data['email'], is_staff=False)
        correctResponse = {
            'token': str(Token.objects.get(user=user)),
            'username': user.username
        }
        self.assertEqual(correctResponse, responseData)

    def test_correct_register_one_other_user(self):
        """Testing a legitimate registration with one other user."""
        PlayerFactory()
        data = {'email': 'testEmail@gmail.com', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)
        user = Player.objects.get(email=data['email'], is_staff=False)
        correctResponse = {
            'token': str(Token.objects.get(user=user)),
            'username': user.username
        }
        self.assertEqual(correctResponse, responseData)

    def test_register_bad_email(self):
        """Testing a bad register with bad email param."""
        data = {'email': 'test', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'email': ['Enter a valid email address.']}
        self.assertEqual(correctResponse, responseData)

    def test_register_no_email(self):
        """Testing a bad register with no email param."""
        data = {'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'email': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_register_bad_password_length(self):
        """Testing a bad register with bad password length."""
        data = {'email': 'willFail@gmail.com', 'password': 't'}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'password': ['This password is too short. It must contain at least 8 characters.',
                         'This password is too common.']
        }
        self.assertEqual(correctResponse, responseData)

    def test_register_bad_password_common(self):
        """Testing a bad register with bad password too common."""
        data = {'email': 'willFail@gmail.com', 'password': 'password'}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'password': ['This password is too common.']}
        self.assertEqual(correctResponse, responseData)

    def test_register_bad_password_numeric(self):
        """Testing a bad register with bad password that's only numbers."""
        data = {'email': 'willFail@gmail.com', 'password': '234238483'}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'password': ['This password is entirely numeric.']}
        self.assertEqual(correctResponse, responseData)

    def test_register_no_password(self):
        """Testing a bad register with no password param."""
        data = {'email': 'willFail@gmail.com'}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'password': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_register_no_email_or_password(self):
        """Testing a bad register with no email or password params."""
        data = {}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'password': ['This field is required.'],
            'email': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_register_email_in_use(self):
        user = PlayerFactory()
        data = {'email': user.email, 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('register')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'email': ['Email already in use.']}
        self.assertEqual(correctResponse, responseData)
