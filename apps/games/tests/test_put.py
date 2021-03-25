import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..serializers import GameSerializer, PointSerializer
from .comparers import checkGameMatch

# Change player and make sure points change too
# Make sure the id doesn't change for games after edits


class Test_Game_PUT(TestCase):
    def test_put_change_p1(self):
        """
        Testing one simple put
        Changing player one
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        gameModel.playerOne = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerOne'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerTwo)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_p2(self):
        """
        Testing one simple put
        Changing player two
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player two
        newPlayer = CustomUserFactory()
        gameModel.playerTwo = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerTwo'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerThree)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_p3(self):
        """
        Testing one simple put
        Changing player three
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player three
        newPlayer = CustomUserFactory()
        gameModel.playerThree = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerThree'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerFour)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_p4(self):
        """
        Testing one simple put
        Changing player four
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player four
        newPlayer = CustomUserFactory()
        gameModel.playerFour = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerFour'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_p1_as_new_player(self):
        """
        Testing one simple put
        Changing player one, but as the new player, which isn't allowed
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        gameModel.playerOne = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerOne'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=newPlayer)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('gameId' in responseData)
        estr = 'Game id not found: {}'.format(gameModel.id)
        self.assertEqual(responseData['gameId'], [estr])

    def test_put_change_p2_as_new_player(self):
        """
        Testing one simple put
        Changing player two, but as the new player, which isn't allowed
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player two
        newPlayer = CustomUserFactory()
        gameModel.playerTwo = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerTwo'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=newPlayer)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('gameId' in responseData)
        estr = 'Game id not found: {}'.format(gameModel.id)
        self.assertEqual(responseData['gameId'], [estr])

    def test_put_change_p3_as_new_player(self):
        """
        Testing one simple put
        Changing player three, but as the new player, which isn't allowed
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player three
        newPlayer = CustomUserFactory()
        gameModel.playerThree = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerThree'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=newPlayer)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('gameId' in responseData)
        estr = 'Game id not found: {}'.format(gameModel.id)
        self.assertEqual(responseData['gameId'], [estr])

    def test_put_change_p4_as_new_player(self):
        """
        Testing one simple put
        Changing player four, but as the new player, which isn't allowed
        """
        gameModel = GameFactory()
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)

        # Subbing the new player for player four
        newPlayer = CustomUserFactory()
        gameModel.playerFour = newPlayer

        gameModelData = GameSerializer(gameModel).data
        gameModelData['playerFour'] = newPlayer.username
        pointModelsData = PointSerializer(pointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=newPlayer)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('gameId' in responseData)
        estr = 'Game id not found: {}'.format(gameModel.id)
        self.assertEqual(responseData['gameId'], [estr])

    def test_put_change_points_as_p1(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P2
        """
        gameModel = GameFactory()
        PointFactory.create_batch(scorer=gameModel.playerOne,
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        newPointModels = PointFactory.build_batch(scorer=gameModel.playerTwo,
                                                  typeOfPoint='SS', size=3,
                                                  game=gameModel)

        # Changing the points to just one self sink by the editing player
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(newPointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_points_as_p2(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P2
        """
        gameModel = GameFactory()
        PointFactory.create_batch(scorer=gameModel.playerTwo,
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        newPointModels = PointFactory.build_batch(scorer=gameModel.playerThree,
                                                  typeOfPoint='SS', size=3,
                                                  game=gameModel)

        # Changing the points to just one self sink by the editing player
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(newPointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerTwo)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_points_as_p3(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P2
        """
        gameModel = GameFactory()
        PointFactory.create_batch(scorer=gameModel.playerTwo,
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        newPointModels = PointFactory.build_batch(scorer=gameModel.playerThree,
                                                  typeOfPoint='SS', size=3,
                                                  game=gameModel)

        # Changing the points to just one self sink by the editing player
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(newPointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerThree)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_put_change_points_as_p4(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P3
        """
        gameModel = GameFactory()
        PointFactory.create_batch(scorer=gameModel.playerTwo,
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        newPointModels = PointFactory.build_batch(scorer=gameModel.playerThree,
                                                  typeOfPoint='SS', size=3,
                                                  game=gameModel)

        # Changing the points to just one self sink by the editing player
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(newPointModels, many=True).data
        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerFour)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.put(url, format='json')

        self.assertEqual(response.status_code, 401)
