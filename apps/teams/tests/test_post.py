import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import TeamFactory
from ..serializers import TeamSerializer
from .comparers import checkTeamMatch


class Test_Team_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        teamCaptain = CustomUserFactory()
        teammate = CustomUserFactory()
        teamModel = TeamFactory.build(teamCaptain=teamCaptain,
                                      teammate=teammate)
        teamModelData = TeamSerializer(teamModel).data

        data = {'team': teammate.username}

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=teamCaptain)
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        avoid = ['id', 'timeRequested', 'timeRespondedTo']
        teamMatched = checkTeamMatch(responseData, teamModelData,
                                     toAvoid=avoid)
        self.assertEqual('valid', teamMatched)

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('team_list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
