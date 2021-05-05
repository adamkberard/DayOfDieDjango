import json
import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from ..models import CustomUser
from .factories import CustomUserFactory

from apps.friends.models import Friend
from apps.friends.serializers import FriendSerializer
from apps.games.models import Game, Point
from apps.games.serializers import GameSerializer, PointSerializer


class Test_Login_View(TestCase):
    def test_correct_login_no_data(self):
        """Testing a legitimate login with no games, friends, or other users."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': "pass4user"}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

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

        # Make sure things went well first
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        # Make sure all the fields are there
        self.checkLoginFields(responseData)

        self.checkLoginData(responseData, check_against_dict)

    def test_correct_login_one_other_user(self):
        """Testing a legitimate login with one other user, no friends or games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': "pass4user"}

        otherUser = CustomUserFactory()

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

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

        # Make sure things went well first
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        # Make sure all the fields are there
        self.checkLoginFields(responseData)

        self.checkLoginData(responseData, check_against_dict)

    def test_correct_login_one_friend(self):
        """Testing a legitimate login with one other user, one friend and no games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': "pass4user"}

        otherUser = CustomUserFactory()
        friendModel = Friend.objects.create(team_captain=userModel, teammate=otherUser)

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = []
        check_against_friends = [FriendSerializer(friendModel).data]
        check_against_all_usernames = [userModel.username, otherUser.username]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # Make sure things went well first
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        # Make sure all the fields are there
        self.checkLoginFields(responseData)

        self.checkLoginData(responseData, check_against_dict)

    def test_correct_login_two_friend(self):
        """Testing a legitimate login with one other user, one friend and no games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': "pass4user"}

        otherUser = CustomUserFactory()
        otherUserTwo = CustomUserFactory()
        friendModel = Friend.objects.create(team_captain=userModel, teammate=otherUser)
        friendModelTwo = Friend.objects.create(team_captain=otherUserTwo, teammate=userModel)

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = []
        check_against_friends = [FriendSerializer(friendModel).data, FriendSerializer(friendModelTwo).data]
        check_against_all_usernames = [userModel.username, otherUser.username, otherUserTwo.username]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # Make sure things went well first
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        # Make sure all the fields are there
        self.checkLoginFields(responseData)

        self.checkLoginData(responseData, check_against_dict)

    def test_correct_login_one_friend_many_users(self):
        """Testing a legitimate login with many other users, one friend and no games."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': "pass4user"}

        otherUser = CustomUserFactory()
        friendModel = Friend.objects.create(team_captain=userModel, teammate=otherUser)

        # The response we want
        check_against_all_usernames = [userModel.username, otherUser.username]
        for i in range(10):
            check_against_all_usernames.append(CustomUserFactory().username)

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # Make sure things went well first
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        # Make sure all the fields are there
        self.checkLoginFields(responseData)

        # The response we want
        check_against_user = {
            'username': userModel.username,
            'email': userModel.email,
            'uuid': str(userModel.uuid),
            'token': str(Token.objects.get(user=userModel))
        }
        check_against_games = []
        check_against_friends = [FriendSerializer(friendModel).data]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }
        self.checkLoginData(responseData, check_against_dict)

    def test_correct_login_three_friends_one_game(self):
        """Testing a legitimate login with three friends and one game."""
        userModel = CustomUserFactory()
        data = {'email': userModel.email, 'password': "pass4user"}

        playerTwo = CustomUserFactory()
        playerThree = CustomUserFactory()
        playerFour = CustomUserFactory()
        friendModelTwo = Friend.objects.create(team_captain=userModel, teammate=playerTwo)
        friendModelThree = Friend.objects.create(team_captain=userModel, teammate=playerThree)
        friendModelFour = Friend.objects.create(team_captain=userModel, teammate=playerFour)
        friendModelFive = Friend.objects.create(team_captain=playerThree, teammate=playerFour)

        gameModel = Game.objects.create(
            team_one=friendModelTwo,
            team_two=friendModelFive,
            team_one_score=11,
            team_two_score=9,
            time_started=datetime.datetime.now(),
            time_ended=datetime.datetime.now(),
            confirmed=
        )

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        # Make sure things went well first
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        # Make sure all the fields are there
        self.checkLoginFields(responseData)

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
            userModel.username, playerTwo.username, playerThree.username, playerFour.username
        ]
        check_against_dict = {
            'user': check_against_user,
            'games': check_against_games,
            'friends': check_against_friends,
            'all_usernames': check_against_all_usernames
        }
        self.checkLoginData(responseData, check_against_dict)

    # Helper Functions
    def checkUser(self, data, check_against_data):
        fields = ['email', 'username', 'uuid', 'token']

        for field in fields:
            self.assertTrue(field in data)
            self.assertEqual(data.get(field), check_against_data.get(field))

    def checkGames(self, data, check_against_data):
        fields = [
            'points', 'team_one', 'team_two', 'time_started', 'time_ended', 'uuid', 'type',
            'team_one_score', 'team_two_score', 'confirmed'
        ]

        self.assertEqual(len(data), len(check_against_data))
        for i in range(len(data)):
            for field in fields:
                self.assertTrue(field in data[i])
                self.assertEqual(data[i].get(field), check_against_data[i].get(field))

    def checkFriends(self, data, check_against_data):
        fields = [
            'uuid', 'status', 'team_name', 'wins', 'losses', 'league'
        ]

        self.assertEqual(len(data), len(check_against_data))
        for i in range(len(data)):
            for field in fields:
                self.assertTrue(field in data[i])
                self.assertEqual(data[i].get(field), check_against_data[i].get(field))

                # Check the two users seperately
                self.assertTrue('team_captain' in data[i])
                self.assertTrue('teammate' in data[i])

                team_captain = data[i].get('team_captain')
                teammate = data[i].get('teammate')

                self.assertEqual(team_captain['username'], check_against_data[i].get('team_captain')['username'])
                self.assertEqual(team_captain['uuid'], check_against_data[i].get('team_captain')['uuid'])
                self.assertEqual(teammate['username'], check_against_data[i].get('teammate')['username'])
                self.assertEqual(teammate['uuid'], check_against_data[i].get('teammate')['uuid'])


    def checkAllUsernames(self, data, check_against_data):
        self.assertEqual(len(data), len(check_against_data))
        # Need to make sure they're the same someday

        for username in check_against_data:
            try:
                data.remove(username)
            except ValueError:
                self.fail('Username list didnt match.')

    def checkLoginFields(self, data):
        self.assertTrue('user' in data)
        self.assertTrue('games' in data)
        self.assertTrue('friends' in data)
        self.assertTrue('all_usernames' in data)

    def checkLoginData(self, data, check_against_data):
        self.checkUser(data['user'], check_against_data['user'])
        self.checkGames(data['games'], check_against_data['games'])
        self.checkFriends(data['friends'], check_against_data['friends'])
        self.checkAllUsernames(data['all_usernames'], check_against_data['all_usernames'])
