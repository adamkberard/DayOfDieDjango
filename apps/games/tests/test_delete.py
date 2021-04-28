import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..models import Game, Point


class Test_Game_DELETE(TestCase):
    def test_simple_delete(self):
        """
        Testing a simple delete of a game and it's points
        """
        gameModel = GameFactory()
        PointFactory.create_batch(scorer=gameModel.playerOne,
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)
        response = client.delete(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Game.objects.filter(id=gameModel.id).count(), 0)
        self.assertEqual(Point.objects.filter(game=gameModel).count(), 0)

    def test_delete_game_not_in(self):
        """
        Testing a simple delete but on a game the user wasn't in
        """
        otherPlayer = CustomUserFactory()
        gameModel = GameFactory()

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=otherPlayer)
        response = client.delete(url)

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        estr = 'Game id not found: {}'.format(gameModel.id)
        self.assertEqual(responseData['gameId'], [estr])

    def test_bad_litter_id(self):
        """
        Testing a simple delete with no litter id
        """
        user = CustomUserFactory()
        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': 0})
        client.force_authenticate(user=user)
        response = client.delete(url)

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        estr = 'Game id not found: {}'.format(0)
        self.assertEqual(responseData['gameId'], [estr])

    def test_no_authentication(self):
        """
        Trying to PUT litter without any user auth
        """
        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': 0})
        response = client.delete(url)

        self.assertEqual(response.status_code, 401)
