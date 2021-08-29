from datetime import datetime, timedelta

import pytz
from django.urls import reverse
from rest_framework.test import APIClient

from apps.friends.models import Friend
from apps.my_auth.tests.factories import CustomUserFactory

from ..models import Game, Point
from ..serializers import GameSerializer
from .checkers import GameTesting
from .factories import GameFactory


class Test_Game_URL_Params(GameTesting):

    def test_game_request_missing_time_started(self):
        """Testing a bad game request missing the time started param."""
        gameModel = GameFactory()
        data = {
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'time_started': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_time_ended(self):
        """Testing a bad game request missing the time ended param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'time_ended': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_player_one(self):
        """Testing a bad game request missing the player one param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'playerOne': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_player_two(self):
        """Testing a bad game request missing the player two param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'playerTwo': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_player_three(self):
        """Testing a bad game request missing the player three param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'playerThree': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_player_four(self):
        """Testing a bad game request missing the player four param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'playerFour': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_team_one_score(self):
        """Testing a bad game request missing the team one score param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_two_score': gameModel.team_two_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'team_one_score': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_team_two_score(self):
        """Testing a bad game request missing the team two score param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.team_one.team_captain.uuid,
            'playerTwo': gameModel.team_one.team_captain.uuid,
            'playerThree': gameModel.team_one.team_captain.uuid,
            'playerFour': gameModel.team_one.team_captain.uuid,
            'team_one_score': gameModel.team_one_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'team_two_score': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_no_params(self):
        """Testing a bad game request with no params."""
        gameModel = GameFactory()
        data = {}

        client = APIClient()
        client.force_authenticate(user=gameModel.team_one.team_captain)
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'time_started': ['This field is required.'],
            'time_ended': ['This field is required.'],
            'playerOne': ['This field is required.'],
            'playerTwo': ['This field is required.'],
            'playerThree': ['This field is required.'],
            'playerFour': ['This field is required.'],
            'team_one_score': ['This field is required.'],
            'team_two_score': ['This field is required.'],
        }
        self.assertEqual(correctResponse, responseData)


class Test_Create_Game(GameTesting):

    def test_model_equality(self):
        p1 = CustomUserFactory()
        p2 = CustomUserFactory()
        team_one = Friend(team_captain=p1, teammate=p2)
        team_two = Friend(team_captain=p2, teammate=p1)
        team_three = Friend(team_captain=p1, teammate=p2)

        self.assertEqual(team_one, team_two)
        self.assertEqual(team_two, team_three)
        self.assertEqual(team_three, team_one)

    def test_success_same_player_order_no_points(self):
        """Testing creating a game with the players in the right order and no points."""
        time_started = datetime.now(pytz.timezone('America/Los_Angeles'))
        time_ended = time_started + timedelta(minutes=25)
        # ISO 8601
        time_started_iso = time_started.isoformat()
        time_ended_iso = time_ended.isoformat()

        players = [
            CustomUserFactory(),
            CustomUserFactory(),
            CustomUserFactory(),
            CustomUserFactory()
        ]
        data = {
            'time_started': time_started_iso,
            'time_ended': time_ended_iso,
            'playerOne': players[0].uuid,
            'playerTwo': players[1].uuid,
            'playerThree': players[2].uuid,
            'playerFour': players[3].uuid,
            'team_one_score': 11,
            'team_two_score': 9
        }

        client = APIClient()
        client.force_authenticate(user=players[0])
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        # The response we want
        team_one = Friend.objects.get_friendship(players[0], players[1])
        team_two = Friend.objects.get_friendship(players[2], players[3])
        gameModel = Game.objects.get(team_one=team_one, time_started=time_started)

        # Make sure game model is okay
        self.assertEqual(gameModel.time_started, time_started)
        self.assertEqual(gameModel.time_ended, time_ended)
        self.assertEqual(gameModel.team_one, team_one)
        self.assertEqual(gameModel.team_two, team_two)
        self.assertEqual(gameModel.team_one_score, 11)
        self.assertEqual(gameModel.team_two_score, 9)
        self.assertEqual(gameModel.confirmed, False)

        # Make the dict to compare return to
        correctResponse = GameSerializer(gameModel).data
        correctResponse['points'] = []

        self.assertEqual(correctResponse, responseData)

    def test_success_different_player_order_no_points(self):
        """Testing creating a game with the players in the opposite order and no points.
            I do this because of how teams are searched for and created. Not sure if it
            actually matters now tbh."""
        time_started = datetime.now(pytz.timezone('America/Los_Angeles'))
        time_ended = time_started + timedelta(minutes=25)
        # ISO 8601
        time_started_iso = time_started.isoformat()
        time_ended_iso = time_ended.isoformat()

        players = [
            CustomUserFactory(),
            CustomUserFactory(),
            CustomUserFactory(),
            CustomUserFactory()
        ]
        data = {
            'time_started': time_started_iso,
            'time_ended': time_ended_iso,
            'playerOne': players[1].uuid,
            'playerTwo': players[0].uuid,
            'playerThree': players[3].uuid,
            'playerFour': players[2].uuid,
            'team_one_score': 11,
            'team_two_score': 9
        }

        client = APIClient()
        client.force_authenticate(user=players[0])
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        # The response we want
        team_one = Friend.objects.get_friendship(players[0], players[1])
        team_two = Friend.objects.get_friendship(players[2], players[3])
        gameModel = Game.objects.get(team_one=team_one, time_started=time_started)

        # Make sure game model is okay
        self.assertEqual(gameModel.time_started, time_started)
        self.assertEqual(gameModel.time_ended, time_ended)
        self.assertEqual(gameModel.team_one, team_one)
        self.assertEqual(gameModel.team_two, team_two)
        self.assertEqual(gameModel.team_one_score, 11)
        self.assertEqual(gameModel.team_two_score, 9)
        self.assertEqual(gameModel.confirmed, False)

        # Make the dict to compare return to
        correctResponse = GameSerializer(gameModel).data
        correctResponse['points'] = []

        self.assertEqual(correctResponse, responseData)

    def test_success_with_points(self):
        """ This is just a game created with the correct amount of corresponding points.
            I'll probably have to eventually start writing tests to ensure the points
            add up to the correct amount. """
        time_started = datetime.now(pytz.timezone('America/Los_Angeles'))
        time_ended = time_started + timedelta(minutes=25)
        # ISO 8601
        time_started_iso = time_started.isoformat()
        time_ended_iso = time_ended.isoformat()

        team_one_score = 11
        team_two_score = 9

        players = [
            CustomUserFactory(),
            CustomUserFactory(),
            CustomUserFactory(),
            CustomUserFactory()
            ]
        points = []
        for i in range(0, team_one_score):
            points.append({
                'type': 'sg',
                'scorer': players[0].uuid
            })
        for i in range(0, team_two_score):
            points.append({
                'type': 'sg',
                'scorer': players[3].uuid
            })

        data = {
            'time_started': time_started_iso,
            'time_ended': time_ended_iso,
            'playerOne': players[1].uuid,
            'playerTwo': players[0].uuid,
            'playerThree': players[3].uuid,
            'playerFour': players[2].uuid,
            'team_one_score': team_one_score,
            'team_two_score': team_two_score,
            'points': points
        }

        client = APIClient()
        client.force_authenticate(user=players[0])
        url = reverse('game_request_create')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        # The response we want
        team_one = Friend.objects.get_friendship(players[0], players[1])
        team_two = Friend.objects.get_friendship(players[2], players[3])
        gameModel = Game.objects.get(team_one=team_one, time_started=time_started)

        # Make sure game model is okay
        self.assertEqual(gameModel.time_started, time_started)
        self.assertEqual(gameModel.time_ended, time_ended)
        self.assertEqual(gameModel.team_one, team_one)
        self.assertEqual(gameModel.team_two, team_two)
        self.assertEqual(gameModel.team_one_score, 11)
        self.assertEqual(gameModel.team_two_score, 9)
        self.assertEqual(gameModel.confirmed, False)

        # Now make sure all the points are correct
        pointModels = Point.objects.filter(game=gameModel)
        self.assertEqual(len(pointModels), len(points))

        correctResponse = GameSerializer(gameModel).data
        self.assertEqual(correctResponse, responseData)

    # def test_invalid_score_no_points
    # def test_invalid_score
    # def test_points_do_not_match_score
    # def test_team_one_points_do_not_match_score
    # def test_team_two_points_do_not_match_score
