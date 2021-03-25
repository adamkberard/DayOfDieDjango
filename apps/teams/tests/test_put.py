import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..factories import TeamFactory
from ..serializers import TeamSerializer
from .comparers import checkTeamMatch

# Change player and make sure points change too
# Make sure the id doesn't change for teams after edits


class Test_Team_PUT(TestCase):
    def test_put_accept_team_as_teammate(self):
        """
        Testing one simple put of accepting a team request
        """
        teamModel = TeamFactory()

        data = {'status': 'accept'}

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=teamModel.teammate)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        teamModel.status = teamModel.ACCEPTED
        teamModelData = TeamSerializer(teamModel).data

        avoid = ['id', 'timeRequested', 'timeRespondedTo']
        teamMatched = checkTeamMatch(responseData, teamModelData,
                                     toAvoid=avoid)
        self.assertEqual('valid', teamMatched)

    def test_put_accept_team_as_teamCaptain(self):
        """
        Testing one simple put of accepting a team request
        """
        teamModel = TeamFactory()

        data = {'status': 'accept'}

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=teamModel.teamCaptain)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        estr = 'Cannot accept a team request as the requester.'
        self.assertEqual(responseData['errors'], [estr])

    def test_put_denied_team_as_requsted(self):
        """
        Testing one simple put of denying a team request as teammate
        """
        teamModel = TeamFactory()

        data = {'status': 'deny'}

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=teamModel.teammate)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        teamModel.status = teamModel.DENIED
        teamModelData = TeamSerializer(teamModel).data

        avoid = ['id', 'timeRequested', 'timeRespondedTo']
        teamMatched = checkTeamMatch(responseData, teamModelData,
                                     toAvoid=avoid)
        self.assertEqual('valid', teamMatched)

    def test_put_denied_team_as_teamCaptain(self):
        """
        Testing one simple put of accepting a team request
        """
        teamModel = TeamFactory()

        data = {'status': 'deny'}

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=teamModel.teamCaptain)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        estr = 'Cannot deny a team request as the requester.'
        self.assertEqual(responseData['errors'], [estr])

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('team_list')
        response = client.put(url, format='json')

        self.assertEqual(response.status_code, 401)
