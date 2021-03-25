import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import TeamFactory
from ..models import Team


class Test_Team_DELETE(TestCase):
    def test_simple_delete(self):
        """
        Testing a simple delete of a team
        """
        teamModel = TeamFactory()

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=teamModel.teamCaptain)
        response = client.delete(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Team.objects.filter(id=teamModel.id).count(), 0)

    def test_delete_team_not_in(self):
        """
        Testing a simple delete but on a team the user wasn't in
        """
        otherPlayer = CustomUserFactory()
        teamModel = TeamFactory()

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=otherPlayer)
        response = client.delete(url)

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        estr = 'Team id not found: {}'.format(teamModel.id)
        self.assertEqual(responseData['teamId'], [estr])

    def test_bad_litter_id(self):
        """
        Testing a simple delete with bad litter id
        """
        player = CustomUserFactory()

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': 0})
        client.force_authenticate(user=player)
        response = client.delete(url)

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        estr = 'Team id not found: {}'.format(0)
        self.assertEqual(responseData['teamId'], [estr])

    def test_no_authentication(self):
        """
        Trying to PUT litter without any user auth
        """
        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': 0})
        response = client.delete(url)

        self.assertEqual(response.status_code, 401)
