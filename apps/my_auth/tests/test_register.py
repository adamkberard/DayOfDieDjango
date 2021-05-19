import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import CustomUser
from .checkers import Auth_Testing_Helpers
from .factories import DEFAULT_PASSWORD, CustomUserFactory


class Test_Register_View(TestCase):
    helper = Auth_Testing_Helpers()

    def test_correct_register(self):
        """Testing a legitimate registration."""
        data = {'email': 'testEmail@gmail.com', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')
        userModel = CustomUser.objects.get(email='testEmail@gmail.com')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = []
        check_against_friends = []
        check_against_all_usernames = [userModel.username]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }

        # Check return
        self.helper.checkLoginReturn(response, check_against_dict)

    def test_correct_register_one_other_user(self):
        """Testing a legitimate registration with one other user."""
        otherUser = CustomUserFactory()

        data = {'email': 'testEmail@gmail.com', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')
        userModel = CustomUser.objects.get(email='testEmail@gmail.com')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = []
        check_against_friends = []
        check_against_all_usernames = [userModel.username, otherUser.username]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }

        # Check return
        self.helper.checkLoginReturn(response, check_against_dict)

    def test_correct_register_four_other_users(self):
        """Testing a legitimate registration with four other users."""
        otherUserOne = CustomUserFactory()
        otherUserTwo = CustomUserFactory()
        otherUserThree = CustomUserFactory()
        otherUserFour = CustomUserFactory()

        data = {'email': 'testEmail@gmail.com', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')
        userModel = CustomUser.objects.get(email='testEmail@gmail.com')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = []
        check_against_friends = []
        check_against_all_usernames = [
            userModel.username,
            otherUserOne.username,
            otherUserTwo.username,
            otherUserThree.username,
            otherUserFour.username
        ]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }

        # Check return
        self.helper.checkLoginReturn(response, check_against_dict)

    def test_register_bad_email(self):
        """Testing a bad register with bad email param."""
        data = {'email': 'test', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('email' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['email'], ['Enter a valid email address.'])

    def test_register_no_email(self):
        """Testing a bad register with no email param."""
        data = {'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('email' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['email'], ['This field is required.'])

    def test_register_bad_password_length(self):
        """Testing a bad register with bad password length."""
        data = {'email': 'willFail@gmail.com', 'password': 't'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('password' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['password'],
                         ['This password is too short. It must contain at least 8 characters.',
                          'This password is too common.'])

    def test_register_bad_password_common(self):
        """Testing a bad register with bad password too common."""
        data = {'email': 'willFail@gmail.com', 'password': 'password'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('password' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['password'], ['This password is too common.'])

    def test_register_bad_password_numeric(self):
        """Testing a bad register with bad password that's only numbers."""
        data = {'email': 'willFail@gmail.com', 'password': '234238483'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('password' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['password'], ['This password is entirely numeric.'])

    def test_register_no_password(self):
        """Testing a bad register with no password param."""
        data = {'email': 'willFail@gmail.com'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('password' in responseData)
        # Make sure there's only one error
        self.assertEqual(responseData['password'], ['This field is required.'])

    def test_register_no_email_or_password(self):
        """Testing a bad register with no email or password params."""
        data = {}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('email' in responseData)
        self.assertTrue('password' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['email'], ['This field is required.'])
        self.assertEqual(responseData['password'], ['This field is required.'])
