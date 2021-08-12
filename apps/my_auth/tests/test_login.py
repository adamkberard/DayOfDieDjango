import json
from datetime import datetime, timedelta

import pytz
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.friends.models import Friend
from apps.friends.serializers import FriendSerializer
from apps.games.models import Game
from apps.games.serializers import GameSerializer

from ..serializers import BasicCustomUserSerializer
from .checkers import AuthTesting
from .factories import DEFAULT_PASSWORD, CustomUserFactory


class Test_Login_View(AuthTesting):

    def test_correct_login_no_data(self):
        """Testing a legitimate login with no games, friends, or other users."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_all_usernames = [BasicCustomUserSerializer(userModel).data]
        self.check_against_data = {
            'user': check_against_user,
            'games': [],
            'friends': [],
            'all_users': check_against_all_usernames
        }

        # Check return
        self.assertResponse201()
        self.loadJSONSafely()
        self.assertLoginDataEqual()

    def test_correct_login_one_other_user(self):
        """Testing a legitimate login with one other user, no friends or games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        otherUser = CustomUserFactory()

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_all_usernames = [
            BasicCustomUserSerializer(userModel).data,
            BasicCustomUserSerializer(otherUser).data
        ]
        self.check_against_data = {
            'user': check_against_user,
            'games': [],
            'friends': [],
            'all_users': check_against_all_usernames
        }

        # Check return
        self.assertResponse201()
        self.loadJSONSafely()
        self.assertLoginDataEqual()

    def test_correct_login_one_friend(self):
        """Testing a legitimate login with one other user, one friend and no games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        otherUser = CustomUserFactory()
        friendModel = Friend.objects.create(team_captain=userModel, teammate=otherUser)

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_friends = [FriendSerializer(friendModel).data]
        check_against_all_usernames = [
            BasicCustomUserSerializer(userModel).data,
            BasicCustomUserSerializer(otherUser).data
        ]
        self.check_against_data = {
            'user': check_against_user,
            'games': [],
            'friends': check_against_friends,
            'all_users': check_against_all_usernames
        }

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # Check return
        self.assertResponse201()
        self.loadJSONSafely()
        self.assertLoginDataEqual()

    def test_correct_login_two_friend(self):
        """Testing a legitimate login with one other user, one friend and no games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        otherUser = CustomUserFactory()
        otherUserTwo = CustomUserFactory()
        friendModel = Friend.objects.create(team_captain=userModel, teammate=otherUser)
        friendModelTwo = Friend.objects.create(team_captain=otherUserTwo, teammate=userModel)

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_friends = [
            FriendSerializer(friendModel).data,
            FriendSerializer(friendModelTwo).data
        ]
        check_against_all_usernames = [
            BasicCustomUserSerializer(userModel).data,
            BasicCustomUserSerializer(otherUser).data,
            BasicCustomUserSerializer(otherUserTwo).data,
        ]
        self.check_against_data = {
            'user': check_against_user,
            'games': [],
            'friends': check_against_friends,
            'all_users': check_against_all_usernames
        }

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # Check return
        self.assertResponse201()
        self.loadJSONSafely()
        self.assertLoginDataEqual()

    def test_correct_login_one_friend_many_users(self):
        """Testing a legitimate login with many other users, one friend and no games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        otherUser = CustomUserFactory()
        friendModel = Friend.objects.create(team_captain=userModel, teammate=otherUser)

        # The response we want
        check_against_all_usernames = [
            BasicCustomUserSerializer(userModel).data,
            BasicCustomUserSerializer(otherUser).data
        ]
        for i in range(10):
            check_against_all_usernames.append(BasicCustomUserSerializer(CustomUserFactory()).data)

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_friends = [FriendSerializer(friendModel).data]
        self.check_against_data = {
            'user': check_against_user,
            'games': [],
            'friends': check_against_friends,
            'all_users': check_against_all_usernames
        }

        # Check return
        self.assertResponse201()
        self.loadJSONSafely()
        self.assertLoginDataEqual()

    def test_correct_login_three_friends_one_game(self):
        """Testing a legitimate login with three friends and one game."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': DEFAULT_PASSWORD}

        playerTwo = CustomUserFactory()
        playerThree = CustomUserFactory()
        playerFour = CustomUserFactory()
        friendModelTwo = Friend.objects.create(team_captain=userModel, teammate=playerTwo)
        friendModelThree = Friend.objects.create(team_captain=userModel, teammate=playerThree)
        friendModelFour = Friend.objects.create(team_captain=userModel, teammate=playerFour)
        friendModelFive = Friend.objects.create(team_captain=playerThree, teammate=playerFour)

        # Make times timezone aware
        timezone = pytz.timezone('America/Los_Angeles')
        time_started = timezone.localize(datetime.now() - timedelta(hours=1))
        time_ended = timezone.localize(datetime.now())

        gameModel = Game.objects.create(
            team_one=friendModelTwo,
            team_two=friendModelFive,
            team_one_score=11,
            team_two_score=9,
            time_started=time_started,
            time_ended=time_ended,
            confirmed=False
        )

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        # Check the data of the fields
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = [GameSerializer(gameModel).data]
        check_against_friends = [
            FriendSerializer(friendModelTwo).data,
            FriendSerializer(friendModelThree).data,
            FriendSerializer(friendModelFour).data
        ]
        check_against_all_usernames = [
            BasicCustomUserSerializer(userModel).data,
            BasicCustomUserSerializer(playerTwo).data,
            BasicCustomUserSerializer(playerThree).data,
            BasicCustomUserSerializer(playerFour).data,
        ]
        self.check_against_data = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_users': check_against_all_usernames
        }

        # Check return
        self.assertResponse201()
        self.loadJSONSafely()
        self.assertLoginDataEqual()

    def test_login_bad_email(self):
        """Testing a bad login with bad email param."""
        data = {'email': 'test', 'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_login')
        self.response = client.post(url, data, format='json')

        self.assertResponse400()
        self.check_against_data = {'email': ['Enter a valid email address.']}
        self.fields = ['email']
        self.assertResponseEqual()

    def test_login_no_email(self):
        """Testing a bad login with no email param."""
        data = {'password': DEFAULT_PASSWORD}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('email' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['email'], ['This field is required.'])

    def test_login_no_password(self):
        """Testing a bad login with no password param."""
        data = {'email': 'willFail@gmail.com'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('password' in responseData)
        # Make sure there's only one error
        self.assertEqual(responseData['password'], ['This field is required.'])

    def test_login_no_email_or_password(self):
        """Testing a bad login with no email or password params."""
        data = {}

        client = APIClient()
        url = reverse('my_login')
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
