import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..models import Point


class Test_Game_GET(TestCase):
    def test_get_games_single(self):
        """
        Trying to get all the games a person has played.
        Which is one in this case.
        """

        game = GameFactory()

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), 1)
        game  = responseData[0]
        points = game['points']
        self.assertEqual(game['timeStarted'], game.timeStarted)
        self.assertEqual(game['timeSaved'], game.timeSaved)
        self.assertEqual(game['playerOne'], game.playerOne)
        self.assertEqual(game['playerTwo'], game.playerTwo)
        self.assertEqual(game['playerThree'], game.playerThree)
        self.assertEqual(game['playerFour'], game.playerFour)
        self.assertEqual(len(game['id']), 8)

        self.assertEqual(len(points), game.getTotalPoints())

    def test_get_games_few(self):
        """
        Trying to get all the games a person has logged.
        """
        few = 5
        user = CustomUserFactory()
        games = []
        for i in range(0, few):
            games.append(GameFactory(user=user))

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), few)
        for i in range(0, few):
            game  = responseData[i]['game']
            points = responseData[i]['points']
            self.assertEqual(game['timeStarted'], game.timeStarted)
            self.assertEqual(game['timeSaved'], game.timeSaved)
            self.assertEqual(game['playerOne'], game.playerOne)
            self.assertEqual(game['playerTwo'], game.playerTwo)
            self.assertEqual(game['playerThree'], game.playerThree)
            self.assertEqual(game['playerFour'], game.playerFour)
            self.assertEqual(len(game['id']), 8)

    def test_get_games_many(self):
        few = 15
        user = CustomUserFactory()
        games = []
        for i in range(0, few):
            games.append(GameFactory(user=user))

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), few)
        for i in range(0, few):
            game  = responseData[i]['game']
            points = responseData[i]['points']
            self.assertEqual(game['timeStarted'], game.timeStarted)
            self.assertEqual(game['timeSaved'], game.timeSaved)
            self.assertEqual(game['playerOne'], game.playerOne)
            self.assertEqual(game['playerTwo'], game.playerTwo)
            self.assertEqual(game['playerThree'], game.playerThree)
            self.assertEqual(game['playerFour'], game.playerFour)
            self.assertEqual(len(game['id']), 8)

    def test_get_litter_no_pieces(self):
        """
        Trying to get all the litter a person has logged which is none.
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData, [])

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)


#class Test_My_Litter_GET_Detail(TestCase):
#    def test_get_litter_one_piece(self):
#        """
#        Trying to get a single piece of litter.
#        """
#
#        user = CustomUserFactory()
#        inLitter = LitterFactory(user=user)
#
#        client = APIClient()
#        url = reverse('litter-detail', kwargs={'litterId': inLitter.id})
#        client.force_authenticate(user=user)
#        response = client.get(url)
#        responseData = json.loads(response.content)
#
#        self.assertEqual(responseData['typeOfLitter'], inLitter.typeOfLitter)
#        self.assertEqual(responseData['amount'], inLitter.amount)
#        self.assertTrue(responseData['timeCollected'] is not None)
#        self.assertEqual(len(responseData['id']), 8)
#
#    def test_get_same_litter_twice(self):
#        """
#        Trying to get the same piece of litter twice.
#        """
#        user = CustomUserFactory()
#        client = APIClient()
#        client.force_authenticate(user=user)
#        litter = LitterFactory(user=user)
#        url = reverse('litter-detail', kwargs={'litterId': litter.id})
#
#        for i in range(0, 2):
#            response = client.get(url)
#            responseData = json.loads(response.content)
#
#            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
#            self.assertEqual(responseData['amount'], litter.amount)
#            self.assertTrue(responseData['timeCollected'] is not None)
#            self.assertEqual(len(responseData['id']), 8)
#
#    def test_get_same_litter_many_times(self):
#        """
#        Trying to get all the litter a person has logged many times.
#        Which is just one piece of litter
#        """
#        user = CustomUserFactory()
#        client = APIClient()
#        client.force_authenticate(user=user)
#        litter = LitterFactory(user=user)
#        url = reverse('litter-detail', kwargs={'litterId': litter.id})
#
#        for i in range(0, 100):
#            response = client.get(url)
#            responseData = json.loads(response.content)
#
#            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
#            self.assertEqual(responseData['amount'], litter.amount)
#            self.assertTrue(responseData['timeCollected'] is not None)
#            self.assertEqual(len(responseData['id']), 8)
#
#    def test_get_two_litters(self):
#        """
#        Trying to get all the litter a person has logged.
#        Which is two this time!
#        """
#        user = CustomUserFactory()
#        client = APIClient()
#        client.force_authenticate(user=user)
#
#        for i in range(0, 2):
#            litter = LitterFactory(user=user)
#            url = reverse('litter-detail', kwargs={'litterId': litter.id})
#            response = client.get(url)
#            responseData = json.loads(response.content)
#
#            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
#            self.assertEqual(responseData['amount'], litter.amount)
#            self.assertTrue(responseData['timeCollected'] is not None)
#            self.assertEqual(len(responseData['id']), 8)
#
#
#    def test_get_many_litters(self):
#        """
#        Trying to get all the litter a person has logged.
#        Which is a bunch in this case.
#        """
#        user = CustomUserFactory()
#        client = APIClient()
#        client.force_authenticate(user=user)
#
#        for i in range(0, 100):
#            litter = LitterFactory(user=user)
#            url = reverse('litter-detail', kwargs={'litterId': litter.id})
#            response = client.get(url)
#            responseData = json.loads(response.content)
#
#            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
#            self.assertEqual(responseData['amount'], litter.amount)
#            self.assertTrue(responseData['timeCollected'] is not None)
#            self.assertEqual(len(responseData['id']), 8)
#
#    def test_get_wrong_litter(self):
#        """
#        Trying to get a litter at a bs litter id.
#        """
#        user = CustomUserFactory()
#
#        client = APIClient()
#        url = reverse('litter-detail', kwargs={'litterId': 0})
#        client.force_authenticate(user=user)
#        response = client.get(url)
#        responseData = json.loads(response.content)
#
#        self.assertEqual(responseData['errors']['litterId'],
#                         'Litter id not found: 0')
#
#    def test_get_litter_not_yours(self):
#        """
#        Trying to get litter that isn't theirs
#        """
#        user1 = CustomUserFactory(email='user1')
#        user2 = CustomUserFactory(email='user2')
#        litter = LitterFactory(user=user2)
#
#        client = APIClient()
#        client.force_authenticate(user=user1)
#        url = reverse('litter-detail', kwargs={'litterId': litter.id})
#        response = client.get(url)
#        responseData = json.loads(response.content)
#
#        self.assertEqual(responseData['errors']['litterId'],
#                         'Litter id not found: ' + str(litter.id))
#
#    def test_no_authentication(self):
#        """
#        Trying to get all the litter without any user auth
#        """
#        client = APIClient()
#        user = CustomUserFactory()
#        litter = LitterFactory(user=user)
#        url = reverse('litter-detail', kwargs={'litterId': litter.id})
#        response = client.get(url)
#
#        self.assertEqual(response.status_code, 401)
