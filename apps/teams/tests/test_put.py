import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from tools.ids_encoder import decode_id

from ..factories import TeamFactory

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

        self.assertTrue(response.status_code, 200)
        responseData = json.loads(response.content)

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        teamModel.status = teamModel.ACCEPTED

        self.assertTrue('team' in responseData)
        teamData = responseData['team']

        # Gotta make sure the team id didn't change cuz that would
        # be annoying
        self.assertTrue('id' in teamData)
        self.assertEqual(teamModel.id, decode_id(teamData['id']))

        # First I'll check the date times
        dateFStr = '%Y-%m-%d %H:%M:%S'
        self.assertTrue('timeRequested' in teamData)
        self.assertEqual(teamData['timeRequested'],
                         teamModel.timeRequested.strftime(dateFStr))
        self.assertTrue('timeRespondedTo' in teamData)
        self.assertEqual(teamData['timeRespondedTo'],
                         teamModel.timeRespondedTo.strftime(dateFStr))

        # Then I'll check the players
        self.assertTrue('teamCaptain' in teamData)
        self.assertEqual(teamModel.teamCaptain.username,
                         teamData['teamCaptain'])
        self.assertTrue('teammate' in teamData)
        self.assertEqual(teamModel.teammate.username,
                         teamData['teammate'])

        # Finally make sure we actually changed the status
        self.assertTrue('status' in teamData)
        self.assertTrue(teamModel.status, teamData['status'])

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
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        estr = 'Cannot accept a team request as the teamCaptain.'
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
        responseData = json.loads(response.content)

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        teamModel.status = teamModel.DENIED

        self.assertTrue('team' in responseData)
        teamData = responseData['team']

        # Gotta make sure the team id didn't change cuz that would
        # be annoying
        self.assertTrue('id' in teamData)
        self.assertEqual(teamModel.id, decode_id(teamData['id']))

        # First I'll check the date times
        dateFStr = '%Y-%m-%d %H:%M:%S'
        self.assertTrue('timeRequested' in teamData)
        self.assertEqual(teamData['timeRequested'],
                         teamModel.timeRequested.strftime(dateFStr))
        self.assertTrue('timeRespondedTo' in teamData)
        self.assertEqual(teamData['timeRespondedTo'],
                         teamModel.timeRespondedTo.strftime(dateFStr))

        # Then I'll check the players
        self.assertTrue('teamCaptain' in teamData)
        self.assertEqual(teamModel.teamCaptain.username,
                         teamData['teamCaptain'])
        self.assertTrue('teammate' in teamData)
        self.assertEqual(teamModel.teammate.username,
                         teamData['teammate'])

        # Finally make sure we actually changed the status
        self.assertTrue('status' in teamData)
        self.assertTrue(teamModel.status, teamData['status'])

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
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        estr = 'Cannot deny a team request as the teamCaptain.'
        self.assertEqual(responseData['errors'], [estr])

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('team_list')
        response = client.put(url, format='json')

        self.assertEqual(response.status_code, 401)
