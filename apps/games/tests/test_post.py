import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory
from tools.helperFunctions.testHelperFuncs import pointsMatch

from ..factories import GameFactory, PointFactory
from ..serializers import GameSerializer, PointSerializer


class Test_Game_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory.build(playerOne=plyr[0], playerTwo=plyr[1],
                                      playerThree=plyr[2], playerFour=plyr[3])
        pointModels = PointFactory.build_batch(scorer=plyr[0],
                                               typeOfPoint='PT',
                                               size=11)

        data = {'game': GameSerializer(gameModel).data,
                'points': PointSerializer(pointModels, many=True).data}

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=plyr[0])
        response = client.post(url, data, format='json')
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

    def test_no_posts(self):
        """
        Testing a post with no data
        """

        user = CustomUserFactory()

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=user)
        response = client.post(url, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['game'][0], 'This field is required.')

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
