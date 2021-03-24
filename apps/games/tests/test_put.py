import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory
from tools.helperFunctions.testHelperFuncs import pointsMatch
from tools.ids_encoder import decode_id

from ..factories import GameFactory, PointFactory
from ..serializers import GameSerializer, PointSerializer

# Change player and make sure points change too
# Make sure the id doesn't change for games after edits


class Test_Game_PUT(TestCase):
    def test_put_change_p1(self):
        """
        Testing one simple put
        Changing player one
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[0] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerOne'] = newPlayer.username

        data = {'game': serializedGameData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[1])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        gameModel.playerOne = newPlayer

        self.assertTrue('game' in responseData)
        self.assertTrue('points' in responseData)
        gameData = responseData['game']

        # Gotta make sure the game id didn't change cuz that would be annoying
        self.assertEqual(gameModel.id, decode_id(gameData['id']))

        # First I'll check the date times
        dateFormatString = '%Y-%m-%d %H:%M:%S'
        self.assertEqual(gameData['timeStarted'],
                         gameModel.timeStarted.strftime(dateFormatString))
        self.assertEqual(gameData['timeSaved'],
                         gameModel.timeSaved.strftime(dateFormatString))

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then I'll check the players
        fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
        for field in fields:
            self.assertEqual(gameData[field],
                             getattr(gameModel, field).username)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

    def test_put_change_p2(self):
        """
        Testing one simple put
        Changing player two
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[1] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerTwo'] = newPlayer.username

        data = {'game': serializedGameData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[2])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        gameModel.playerTwo = newPlayer

        self.assertTrue('game' in responseData)
        self.assertTrue('points' in responseData)
        gameData = responseData['game']

        # Gotta make sure the game id didn't change cuz that would be annoying
        self.assertEqual(gameModel.id, decode_id(gameData['id']))

        # First I'll check the date times
        dateFormatString = '%Y-%m-%d %H:%M:%S'
        self.assertEqual(gameData['timeStarted'],
                         gameModel.timeStarted.strftime(dateFormatString))
        self.assertEqual(gameData['timeSaved'],
                         gameModel.timeSaved.strftime(dateFormatString))

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then I'll check the players
        fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
        for field in fields:
            self.assertEqual(gameData[field],
                             getattr(gameModel, field).username)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

    def test_put_change_p3(self):
        """
        Testing one simple put
        Changing player three
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[2] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerThree'] = newPlayer.username

        data = {'game': serializedGameData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[3])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        gameModel.playerThree = newPlayer

        self.assertTrue('game' in responseData)
        self.assertTrue('points' in responseData)
        gameData = responseData['game']

        # Gotta make sure the game id didn't change cuz that would be annoying
        self.assertEqual(gameModel.id, decode_id(gameData['id']))

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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

    def test_put_change_p4(self):
        """
        Testing one simple put
        Changing player four
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[3] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerFour'] = newPlayer.username

        data = {'game': serializedGameData}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[0])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        gameModel.playerFour = newPlayer

        self.assertTrue('game' in responseData)
        self.assertTrue('points' in responseData)
        gameData = responseData['game']

        # Gotta make sure the game id didn't change cuz that would be annoying
        self.assertEqual(gameModel.id, decode_id(gameData['id']))

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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

    def test_put_change_p1_as_new_player(self):
        """
        Testing one simple put
        Changing player one, but as the new player, which isn't allowed
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[0] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerOne'] = newPlayer.username

        data = {'game': GameSerializer(gameModel).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[0])
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
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[1] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerTwo'] = newPlayer.username

        data = {'game': GameSerializer(gameModel).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[1])
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
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[2] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerThree'] = newPlayer.username

        data = {'game': GameSerializer(gameModel).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[2])
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
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])

        # Subbing the new player for player one
        newPlayer = CustomUserFactory()
        plyr[3] = newPlayer

        serializedGameData = GameSerializer(gameModel).data
        serializedGameData['playerFour'] = newPlayer.username

        data = {'game': GameSerializer(gameModel).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[3])
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
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        PointFactory.create_batch(scorer=plyr[0],
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        editedPointModels = PointFactory.build_batch(scorer=plyr[1],
                                                     typeOfPoint='SS', size=3,
                                                     game=gameModel)

        # Changing the points to just one self sink by the editing player
        data = {'points': PointSerializer(editedPointModels, many=True).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[0])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Checking everything just to be sure the game didn't change at all
        # I guess
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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(editedPointModels, pointsData))

    def test_put_change_points_as_p2(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P2
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        PointFactory.create_batch(scorer=plyr[0],
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        editedPointModels = PointFactory.build_batch(scorer=plyr[1],
                                                     typeOfPoint='SS', size=3,
                                                     game=gameModel)

        # Changing the points to just one self sink by the editing player
        data = {'points': PointSerializer(editedPointModels, many=True).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[1])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Checking everything just to be sure the game didn't change at all
        # I guess
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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(editedPointModels, pointsData))

    def test_put_change_points_as_p3(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P2
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        PointFactory.create_batch(scorer=plyr[0],
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        editedPointModels = PointFactory.build_batch(scorer=plyr[1],
                                                     typeOfPoint='SS', size=3,
                                                     game=gameModel)

        # Changing the points to just one self sink by the editing player
        data = {'points': PointSerializer(editedPointModels, many=True).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[2])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Checking everything just to be sure the game didn't change at all
        # I guess
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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(editedPointModels, pointsData))

    def test_put_change_points_as_p4(self):
        """
        Testing one simple put
        Changing the points from 11 PT's to 3 SS's as P3
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        PointFactory.create_batch(scorer=plyr[0],
                                  typeOfPoint='PT', size=3,
                                  game=gameModel)
        editedPointModels = PointFactory.build_batch(scorer=plyr[2],
                                                     typeOfPoint='SS', size=3,
                                                     game=gameModel)

        # Changing the points to just one self sink by the editing player
        data = {'points': PointSerializer(editedPointModels, many=True).data}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[3])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Checking everything just to be sure the game didn't change at all
        # I guess
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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(editedPointModels, pointsData))

    def test_no_puts(self):
        """
        Testing a put with no data
        """

        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory(playerOne=plyr[0], playerTwo=plyr[1],
                                playerThree=plyr[2], playerFour=plyr[3])
        pointModels = PointFactory.create_batch(scorer=plyr[0],
                                                typeOfPoint='PT', size=3,
                                                game=gameModel)

        # Not changing anything should result in just getting the game back
        data = {}

        client = APIClient()
        url = reverse('game_detail', kwargs={'gameId': gameModel.id})
        client.force_authenticate(user=plyr[0])
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        # Checking everything just to be sure the game didn't change at all
        # I guess
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

        # Check stat keeping record
        self.assertTrue('statType' in gameData)
        self.assertEqual(gameData['statType'], gameModel.statType)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both
        # lists are empty
        self.assertTrue(pointsMatch(pointModels, pointsData))

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.put(url, format='json')

        self.assertEqual(response.status_code, 401)
