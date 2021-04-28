import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..serializers import GameSerializer, PointSerializer
from .comparers import checkGameMatch


class Test_Game_GET(TestCase):
    def test_get_games_single(self):
        """
        Trying to get all the games a person has played.
        Which is one in this case.
        """
        gameModel = GameFactory()
        pointModels = PointFactory.create_batch(scorer=gameModel.playerOne,
                                                typeOfPoint='PT', size=11,
                                                game=gameModel)
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(pointModels, many=True).data

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=gameModel.playerOne)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('games' in responseData)
        self.assertEqual(len(responseData['games']), 1)
        gameSet = responseData['games'][0]
        gameMatched = checkGameMatch(gameSet, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_get_games_many(self):
        """
        Trying to get all the games a person has played.
        Which is twelve in this case.
        """
        numGames = 5
        player = CustomUserFactory()
        gameModels = GameFactory.create_batch(playerOne=player, size=numGames)
        gameModelDatas = GameSerializer(gameModels, many=True).data

        pointModelDatas = []
        for gameModel in gameModels:
            pointModels = PointFactory.create_batch(scorer=player,
                                                    typeOfPoint='PT', size=11,
                                                    game=gameModel)
            temp = PointSerializer(pointModels, many=True).data
            pointModelDatas.append(temp)

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=gameModel.playerOne)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('games' in responseData)
        gamesData = responseData['games']

        self.assertEqual(len(gamesData), numGames)
        for i in range(0, numGames):
            gameMatched = checkGameMatch(gamesData[i], gameModelDatas[i],
                                         pointModelDatas[i])
            self.assertEqual('valid', gameMatched)

    def test_get_no_games(self):
        """
        Trying to get all the games a person has logged which is none.
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=user)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('games' in responseData)
        self.assertEqual(len(responseData['games']), 0)

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)


class Test_Game_GET_Detail(TestCase):
    def test_get_game(self):
        """
        Trying to get a single game that is also the players only
        game
        """
        gameModel = GameFactory()
        pointModels = PointFactory.create_batch(scorer=gameModel.playerOne,
                                                typeOfPoint='PT', size=11,
                                                game=gameModel)
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(pointModels, many=True).data

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData)
        self.assertEqual('valid', gameMatched)

    def test_get_game_twice(self):
        """
        Trying to get a single game that is the players only game twice.
        """
        gameModel = GameFactory()
        pointModels = PointFactory.create_batch(scorer=gameModel.playerOne,
                                                typeOfPoint='PT', size=11,
                                                game=gameModel)
        gameModelData = GameSerializer(gameModel).data
        pointModelsData = PointSerializer(pointModels, many=True).data

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)

        for i in range(0, 2):
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            responseData = json.loads(response.content)
            self.assertEqual(len(responseData), 1)

            gameMatched = checkGameMatch(responseData, gameModelData,
                                         pointModelsData)
            self.assertEqual('valid', gameMatched)

    def test_get_games_of_many(self):
        """
        Trying to get all the games of many
        """
        numGames = 5
        player = CustomUserFactory()
        gameModels = GameFactory.create_batch(playerOne=player, size=numGames)
        gameModelDatas = GameSerializer(gameModels, many=True).data

        pointModelDatas = []
        for gameModel in gameModels:
            pointModels = PointFactory.create_batch(scorer=player,
                                                    typeOfPoint='PT', size=11,
                                                    game=gameModel)
            temp = PointSerializer(pointModels, many=True).data
            pointModelDatas.append(temp)

        client = APIClient()
        client.force_authenticate(user=gameModel.playerOne)

        for i in range(0, numGames):
            gameModelData = gameModelDatas[i]
            pointModelsData = pointModelDatas[i]
            url = reverse('game_detail', kwargs={'gameId': gameModels[i].id})
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            responseData = json.loads(response.content)

            gameMatched = checkGameMatch(responseData, gameModelData,
                                         pointModelsData)
            self.assertEqual('valid', gameMatched)

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
