from datetime import datetime, timedelta

import dateutil.parser
import pytz
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.tests.factories import PlayerFactory
from apps.teams.models import Team

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
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
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
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
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
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
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
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
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
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
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
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'playerFour': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_home_team_score(self):
        """Testing a bad game request missing the team one score param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'away_team_score': gameModel.away_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'home_team_score': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_away_team_score(self):
        """Testing a bad game request missing the team two score param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'away_team_score': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_missing_points(self):
        """Testing a bad game request missing the team two score param."""
        gameModel = GameFactory()
        data = {
            'time_started': gameModel.time_started,
            'time_ended': gameModel.time_ended,
            'playerOne': gameModel.home_team.team_captain.uuid,
            'playerTwo': gameModel.home_team.team_captain.uuid,
            'playerThree': gameModel.home_team.team_captain.uuid,
            'playerFour': gameModel.home_team.team_captain.uuid,
            'home_team_score': gameModel.home_team_score,
            'away_team_score': gameModel.away_team_score,
        }

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'points': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_game_request_no_params(self):
        """Testing a bad game request with no params."""
        gameModel = GameFactory()
        data = {}

        client = APIClient()
        client.force_authenticate(user=gameModel.home_team.team_captain)
        url = reverse('GameListCreate')
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
            'home_team_score': ['This field is required.'],
            'away_team_score': ['This field is required.'],
            'points': ['This field is required.']
        }
        self.assertEqual(correctResponse, responseData)


class Test_Create_Game(GameTesting):

    def test_model_equality(self):
        p1 = PlayerFactory()
        p2 = PlayerFactory()
        home_team = Team(team_captain=p1, teammate=p2)
        away_team = Team(team_captain=p2, teammate=p1)
        team_three = Team(team_captain=p1, teammate=p2)

        self.assertEqual(home_team, away_team)
        self.assertEqual(away_team, team_three)
        self.assertEqual(team_three, home_team)

    def test_success_same_player_order_no_points(self):
        """Testing creating a game with the players in the right order and no points."""
        time_started = datetime.now(pytz.timezone('America/Los_Angeles'))
        time_ended = time_started + timedelta(minutes=25)
        # ISO 8601
        time_started_iso = time_started.isoformat()
        time_ended_iso = time_ended.isoformat()

        players = [
            PlayerFactory(),
            PlayerFactory(),
            PlayerFactory(),
            PlayerFactory()
        ]
        data = {
            'time_started': time_started_iso,
            'time_ended': time_ended_iso,
            'playerOne': players[0].uuid,
            'playerTwo': players[1].uuid,
            'playerThree': players[2].uuid,
            'playerFour': players[3].uuid,
            'home_team_score': 11,
            'away_team_score': 9,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=players[0])
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        # The response we want
        home_team = Team.objects.get_team(players[0], players[1])
        away_team = Team.objects.get_team(players[2], players[3])
        gameModel = Game.objects.get(home_team=home_team, time_started=time_started)

        # Make sure game model is okay
        self.assertEqual(gameModel.time_started, time_started)
        self.assertEqual(gameModel.time_ended, time_ended)
        self.assertEqual(gameModel.home_team, home_team)
        self.assertEqual(gameModel.away_team, away_team)
        self.assertEqual(gameModel.home_team_score, 11)
        self.assertEqual(gameModel.away_team_score, 9)
        self.assertEqual(gameModel.confirmed, False)

        # Make the dict to compare return to
        correctResponse = GameSerializer(gameModel).data
        correctResponse['points'] = []

        # Compare the time's manually
        correctResponse.pop('time_started')
        correctResponse.pop('time_ended')
        responseDataTimeStarted = dateutil.parser.isoparse(responseData.pop('time_started'))
        responseDataTimeEnded = dateutil.parser.isoparse(responseData.pop('time_ended'))
        self.assertEqual(gameModel.time_started, responseDataTimeStarted)
        self.assertEqual(gameModel.time_ended, responseDataTimeEnded)

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
            PlayerFactory(),
            PlayerFactory(),
            PlayerFactory(),
            PlayerFactory()
        ]
        data = {
            'time_started': time_started_iso,
            'time_ended': time_ended_iso,
            'playerOne': players[1].uuid,
            'playerTwo': players[0].uuid,
            'playerThree': players[3].uuid,
            'playerFour': players[2].uuid,
            'home_team_score': 11,
            'away_team_score': 9,
            'points': []
        }

        client = APIClient()
        client.force_authenticate(user=players[0])
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        # The response we want
        home_team = Team.objects.get_team(players[0], players[1])
        away_team = Team.objects.get_team(players[2], players[3])
        gameModel = Game.objects.get(home_team=home_team, time_started=time_started)

        # Make sure game model is okay
        self.assertEqual(gameModel.time_started, time_started)
        self.assertEqual(gameModel.time_ended, time_ended)
        self.assertEqual(gameModel.home_team, home_team)
        self.assertEqual(gameModel.away_team, away_team)
        self.assertEqual(gameModel.home_team_score, 11)
        self.assertEqual(gameModel.away_team_score, 9)
        self.assertEqual(gameModel.confirmed, False)

        # Make the dict to compare return to
        correctResponse = GameSerializer(gameModel).data
        correctResponse['points'] = []

        # Compare the time's manually
        correctResponse.pop('time_started')
        correctResponse.pop('time_ended')
        responseDataTimeStarted = dateutil.parser.isoparse(responseData.pop('time_started'))
        responseDataTimeEnded = dateutil.parser.isoparse(responseData.pop('time_ended'))
        self.assertEqual(gameModel.time_started, responseDataTimeStarted)
        self.assertEqual(gameModel.time_ended, responseDataTimeEnded)

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

        home_team_score = 11
        away_team_score = 9

        players = [
            PlayerFactory(),
            PlayerFactory(),
            PlayerFactory(),
            PlayerFactory()
            ]
        points = []
        for i in range(0, home_team_score):
            points.append({
                'type': 'sg',
                'scorer': players[0].uuid
            })
        for i in range(0, away_team_score):
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
            'home_team_score': home_team_score,
            'away_team_score': away_team_score,
            'points': points
        }

        client = APIClient()
        client.force_authenticate(user=players[0])
        url = reverse('GameListCreate')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        # The response we want
        home_team = Team.objects.get_team(players[0], players[1])
        away_team = Team.objects.get_team(players[2], players[3])
        gameModel = Game.objects.get(home_team=home_team, time_started=time_started)

        # Make sure game model is okay
        self.assertEqual(gameModel.time_started, time_started)
        self.assertEqual(gameModel.time_ended, time_ended)
        self.assertEqual(gameModel.home_team, home_team)
        self.assertEqual(gameModel.away_team, away_team)
        self.assertEqual(gameModel.home_team_score, 11)
        self.assertEqual(gameModel.away_team_score, 9)
        self.assertEqual(gameModel.confirmed, False)

        # Now make sure all the points are correct
        pointModels = Point.objects.filter(game=gameModel)
        self.assertEqual(len(pointModels), len(points))

        correctResponse = GameSerializer(gameModel).data
        # Compare the time's manually
        correctResponse.pop('time_started')
        correctResponse.pop('time_ended')
        responseDataTimeStarted = dateutil.parser.isoparse(responseData.pop('time_started'))
        responseDataTimeEnded = dateutil.parser.isoparse(responseData.pop('time_ended'))
        self.assertEqual(gameModel.time_started, responseDataTimeStarted)
        self.assertEqual(gameModel.time_ended, responseDataTimeEnded)

        self.assertEqual(correctResponse, responseData)

    # def test_invalid_score_no_points
    # def test_invalid_score
    # def test_points_do_not_match_score
    # def test_home_team_points_do_not_match_score
    # def test_away_team_points_do_not_match_score
    # def test_invalid_player_one
    # def test_invalid_player_two
    # def test_invalid_player_three
    # def test_invalid_player_four
