import datetime
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..serializers import GameSerializer, PointSerializer

from ..models import Point


class Test_Game_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        p1 = CustomUserFactory()
        p2 = CustomUserFactory()
        p3 = CustomUserFactory()
        p4 = CustomUserFactory()
        ogGameModel = GameFactory.build(playerOne=p1,
                                        playerTwo=p2,
                                        playerThree=p3,
                                        playerFour=p4)
        ogGameData = GameSerializer(ogGameModel)
        ogPointModels = PointFactory.build_batch(scorer=p1, 
                                                 typeOfPoint='PT',
                                                 size=11)
        ogPointData = PointSerializer(ogPointModels, many=True)

        data = {'game': ogGameData.data,
                'points': ogPointData.data}

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=p1)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertTrue('game' in responseData)
        self.assertTrue('points' in responseData)
        gameData = responseData['game']
        pointsData = responseData['points']

        # First I'll check the date times
        fields = ['timeStarted', 'timeSaved']
        for field in fields:
            self.assertEqual(gameData[field], getattr(ogGameModel, field).strftime("%Y-%m-%d %H:%M:%S"))
        
        # Then I'll check the players
        fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
        for field in fields:
            self.assertEqual(gameData[field], getattr(ogGameModel, field).username)

        # Then make sure we got an ID back
        self.assertTrue(len(gameData['id']) >= 8)

        # Then I check the points
        # To do this I remove matching points until hopefully both 
        # lists are empty
        self.assertTrue(self.pointsMatch(ogPointModels, pointsData))
            
    def pointsMatch(self, models, points):
        if len(models) != len(points):
            return False

        for model in models:
            for point in points:
                if (self.pointMatch(model, point)):
                    points.remove(point)
                    break

        return len(points) == 0

    def pointMatch(self, model, point):
        if model.scorer.username != point['scorer']:
            return False
        if model.typeOfPoint != point['typeOfPoint']:
            return False
        if model.scoredOn is not None:
            if model.scoredOn.username != point['scoredOn']:
                return False
        return True

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
