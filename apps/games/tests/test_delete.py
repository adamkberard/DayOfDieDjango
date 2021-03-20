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
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        PointFactory.create_batch(scorer=plyr[0],
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[0])
        response = client.delete(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['status'], 'okay')
        self.assertEqual(Game.objects.filter(id=gameModel.id).count(), 0)
        self.assertEqual(Point.objects.filter(game=gameModel).count(), 0)

    def test_delete_game_not_in(self):
        """
        Testing a simple delete but on a game the user wasn't in
        """
        plyr = CustomUserFactory.create_batch(size=5)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[4])
        response = client.delete(url)
        responseData = json.loads(response.content)

        errStr = 'Game id not found: '
        self.assertTrue(responseData['error'].startswith(errStr))

    def test_bad_litter_id(self):
        """
        Testing a simple delete with no litter id
        """
        user = CustomUserFactory()
        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': 0})
        client.force_authenticate(user=user)
        response = client.delete(url)
        responseData = json.loads(response.content)

        errStr = 'Game id not found: '
        self.assertTrue(responseData['error'].startswith(errStr))

    def test_no_authentication(self):
        """
        Trying to PUT litter without any user auth
        """
        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': 0})
        response = client.delete(url)

        self.assertEqual(response.status_code, 401)
