import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory
from tools.helperFunctions.testHelperFuncs import pointsMatch
from tools.ids_encoder.converters import HashidsConverter

from ..factories import GameFactory, PointFactory


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

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=gameModel.playerOne)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('game' in responseData[0])
        self.assertTrue('points' in responseData[0])
        gameData = responseData[0]['game']
        pointsData = responseData[0]['points']

        # First I'll check the date times
        dateFormatString = '%Y-%m-%d %H:%M:%S'
        self.assertEqual(gameData['timeStarted'],
                         gameModel.timeStarted.strftime(dateFormatString))
        self.assertEqual(gameData['timeSaved'],
                         gameModel.timeSaved.strftime(dateFormatString))

        # Then I'll check the players
        fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
        for field in fields:
            self.assertEqual(gameData[field],
                             getattr(gameModel, field).username)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(pointModels, pointsData))

    def test_get_games_many(self):
        """
        Trying to get all the games a person has played.
        Which is twelve in this case.
        """
        converter = HashidsConverter()
        plyr = CustomUserFactory.create_batch(size=4)
        gameModels = GameFactory.create_batch(playerOne=plyr[0],
                                              playerTwo=plyr[1],
                                              playerThree=plyr[2],
                                              playerFour=plyr[3],
                                              size=12)
        for gameModel in gameModels:
            pointModels = PointFactory.create_batch(scorer=plyr[0],
                                                    typeOfPoint='PT', size=11,
                                                    game=gameModel)

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=plyr[0])
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        for fullGame in responseData:
            self.assertTrue('game' in fullGame)
            self.assertTrue('points' in fullGame)
            gameData = fullGame['game']
            pointsData = fullGame['points']

            gameModel = None
            # First I find the game it's matched with using the ID
            for game in gameModels:
                if game.id == converter.to_python(gameData['id']):
                    gameModel = game
                    break
            if gameModel is None:
                # If this goes off a matching game wasn't found
                self.assertEqual(True, False)

            # Next I'll check the date times
            dateFormatString = '%Y-%m-%d %H:%M:%S'
            self.assertEqual(gameData['timeStarted'],
                             gameModel.timeStarted.strftime(dateFormatString))
            self.assertEqual(gameData['timeSaved'],
                             gameModel.timeSaved.strftime(dateFormatString))

            # Then I'll check the players
            fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
            for field in fields:
                self.assertEqual(gameData[field],
                                 getattr(gameModel, field).username)

            # Then make sure we got an ID back
            self.assertTrue(len(gameData['id']) >= 8)

            # Then I check the points
            # To do this I remove matching points until hopefully both
            # lists are empty
            self.assertTrue(pointsMatch(pointModels, pointsData))
            gameModels.remove(game)

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

        self.assertEqual(responseData, [])

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

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('game' in responseData)
        self.assertTrue('points' in responseData)
        gameData = responseData['game']
        pointsData = responseData['points']

        # First I'll check the date times
        dateFormatString = '%Y-%m-%d %H:%M:%S'
        self.assertEqual(gameData['timeStarted'],
                         gameModel.timeStarted.strftime(dateFormatString))
        self.assertEqual(gameData['timeSaved'],
                         gameModel.timeSaved.strftime(dateFormatString))

        # Then I'll check the players
        fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
        for field in fields:
            self.assertEqual(gameData[field],
                             getattr(gameModel, field).username)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(pointModels, pointsData))

    def test_get_game_twice(self):
        """
        Trying to get a single game that is the players only game twice.
        """
        gameModel = GameFactory()
        pointModels = PointFactory.create_batch(scorer=gameModel.playerOne,
                                                typeOfPoint='PT', size=11,
                                                game=gameModel)

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=gameModel.playerOne)

        for i in range(0, 2):
            response = client.get(url)
            responseData = json.loads(response.content)
            self.assertEqual(response.status_code, 200)

            self.assertTrue('game' in responseData)
            self.assertTrue('points' in responseData)
            gameData = responseData['game']
            pointsData = responseData['points']

            # First I'll check the date times
            dateFormatString = '%Y-%m-%d %H:%M:%S'
            self.assertEqual(gameData['timeStarted'],
                             gameModel.timeStarted.strftime(dateFormatString))
            self.assertEqual(gameData['timeSaved'],
                             gameModel.timeSaved.strftime(dateFormatString))

            # Then I'll check the players
            fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
            for field in fields:
                self.assertEqual(gameData[field],
                                 getattr(gameModel, field).username)

            # Then make sure we got an ID back
            self.assertTrue(len(gameData['id']) >= 8)

            # Then I check the points
            # To do this I remove matching points until hopefully both
            # lists are empty
            self.assertTrue(pointsMatch(pointModels, pointsData))

    def test_get_games_of_many(self):
        """
        Trying to get all the games of many
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModels = GameFactory.create_batch(playerOne=plyr[0],
                                              playerTwo=plyr[1],
                                              playerThree=plyr[2],
                                              playerFour=plyr[3],
                                              size=12)
        for gameModel in gameModels:
            pointModels = PointFactory.create_batch(scorer=plyr[0],
                                                    typeOfPoint='PT', size=11,
                                                    game=gameModel)

        for gameModel in gameModels:
            client = APIClient()
            url = reverse('game_detail', kwargs={'gameId': gameModel.id})
            client.force_authenticate(user=plyr[0])
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            responseData = json.loads(response.content)

            self.assertTrue('game' in responseData)
            self.assertTrue('points' in responseData)
            gameData = responseData['game']
            pointsData = responseData['points']

            # Next I'll check the date times
            dateFormatString = '%Y-%m-%d %H:%M:%S'
            self.assertEqual(gameData['timeStarted'],
                             gameModel.timeStarted.strftime(dateFormatString))
            self.assertEqual(gameData['timeSaved'],
                             gameModel.timeSaved.strftime(dateFormatString))

            # Then I'll check the players
            fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
            for field in fields:
                self.assertEqual(gameData[field],
                                 getattr(gameModel, field).username)

            # Then make sure we got an ID back
            self.assertTrue(len(gameData['id']) >= 8)

            # Then I check the points
            # To do this I remove matching points until hopefully both
            # lists are empty
            self.assertTrue(pointsMatch(pointModels, pointsData))

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
