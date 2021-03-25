import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..serializers import GameSerializer, PointSerializer
from .comparers import checkGameMatch


class Test_Game_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        plyr = CustomUserFactory.create_batch(size=4)
        gameModel = GameFactory.build(playerOne=plyr[0],
                                      playerTwo=plyr[1],
                                      playerThree=plyr[2],
                                      playerFour=plyr[3])
        gameModelData = GameSerializer(gameModel).data
        pointModels = PointFactory.build_batch(scorer=gameModel.playerOne,
                                               typeOfPoint='PT', size=11,
                                               game=gameModel)
        pointModelsData = PointSerializer(pointModels, many=True).data

        gameModelData['points'] = pointModelsData
        data = {'game': gameModelData}

        client = APIClient()
        url = reverse('game_list')
        client.force_authenticate(user=gameModel.playerOne)
        response = client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 201)

        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('game' in responseData)
        gameMatched = checkGameMatch(responseData, gameModelData,
                                     pointModelsData, ids=False)
        self.assertEqual('valid', gameMatched)

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('game_list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
