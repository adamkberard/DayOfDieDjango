from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.serializers import CustomUserReadSerializer
from apps.my_auth.tests.factories import CustomUserFactory

from .checkers import TeamTesting
from .factories import TeamFactory


class Test_Team_GET(TeamTesting):

    def test_team_get_no_teams(self):
        """Testing a team request get with no teams."""
        user = CustomUserFactory()

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('team_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = []
        self.assertEqual(correctResponse, responseData)

    def test_team_get_one_team_as_team_captain(self):
        """Testing a team request get with one team."""
        teamship = TeamFactory()

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [
            {
                'uuid': str(teamship.uuid),
                'status': teamship.status,
                'team_captain': CustomUserReadSerializer(teamship.team_captain).data,
                'teammate': CustomUserReadSerializer(teamship.teammate).data,
                'wins': 0,
                'losses': 0
            }
        ]
        self.assertEqual(correctResponse, responseData)

    def test_team_get_one_team_as_teammate(self):
        """Testing a team request get with one team."""
        teamship = TeamFactory()

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [
            {
                'uuid': str(teamship.uuid),
                'status': teamship.status,
                'team_captain': CustomUserReadSerializer(teamship.team_captain).data,
                'teammate': CustomUserReadSerializer(teamship.teammate).data,
                'wins': 0,
                'losses': 0
            }
        ]
        self.assertEqual(correctResponse, responseData)

    def test_getting_many_teams(self):
        numTeams = 5
        correctResponse = []
        user = CustomUserFactory()

        for _ in range(numTeams):
            teamship = TeamFactory(team_captain=user)
            correctResponse.append({
                'uuid': str(teamship.uuid),
                'status': teamship.status,
                'team_captain': CustomUserReadSerializer(teamship.team_captain).data,
                'teammate': CustomUserReadSerializer(teamship.teammate).data,
                'wins': 0,
                'losses': 0
            })

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('team_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        self.assertEqual(correctResponse, responseData)

    def test_team_get_one_team_as_team_captain_with_other_teams(self):
        """Testing a team request get with one team."""
        teamship = TeamFactory()
        TeamFactory.create_batch(5)

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [
            {
                'uuid': str(teamship.uuid),
                'status': teamship.status,
                'team_captain': CustomUserReadSerializer(teamship.team_captain).data,
                'teammate': CustomUserReadSerializer(teamship.teammate).data,
                'wins': 0,
                'losses': 0
            }
        ]
        self.assertEqual(correctResponse, responseData)
