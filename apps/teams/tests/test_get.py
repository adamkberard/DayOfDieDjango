import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory
from tools.helperFunctions.testHelperFuncs import fullTeamMatch, teamsMatch

from ..factories import TeamFactory


class Test_Team_GET(TestCase):
    def test_get_teams_single(self):
        """
        Trying to get all the teams a person has. It comes as a list of
        teams. They only have one team in this case.
        """
        player = CustomUserFactory()
        teamModels = []

        numPlayerOne = 1
        numPlayerTwo = 0
        totalTeams = numPlayerOne + numPlayerTwo

        for i in range(0, numPlayerOne):
            teamModels.append(TeamFactory(teamCaptain=player))
        for i in range(0, numPlayerTwo):
            teamModels.append(TeamFactory(teammate=player))

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('teams' in responseData)
        teamsData = responseData['teams']

        # Make sure the number of teams is one
        self.assertEqual(len(teamsData), totalTeams)

        # Now I check all the things
        # Starting with the team username
        self.assertTrue(teamsMatch(teamModels, teamsData))

    def test_get_teams_many(self):
        """
        Trying to get all the teams a person has. It comes as a list of
        teams. They only have one team in this case.
        """
        player = CustomUserFactory()
        teamModels = []

        numPlayerOne = 10
        numPlayerTwo = 10
        totalTeams = numPlayerOne + numPlayerTwo

        for i in range(0, numPlayerOne):
            teamModels.append(TeamFactory(teamCaptain=player))
        for i in range(0, numPlayerTwo):
            teamModels.append(TeamFactory(teammate=player))

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('teams' in responseData)
        teamsData = responseData['teams']

        # Make sure the number of teams is one
        self.assertEqual(len(teamsData), totalTeams)

        # Now I check all the things
        # Starting with the team username
        self.assertTrue(teamsMatch(teamModels, teamsData))

    def test_get_no_teams(self):
        """
        Trying to get all the teams a person has logged which is none.
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=user)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('teams' in responseData)
        self.assertEqual(responseData['teams'], [])

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('team_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)


class Test_Team_GET_Detail(TestCase):
    def test_get_team(self):
        """
        Trying to get a single team based on their id
        """
        teamModel = TeamFactory()

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=teamModel.teamCaptain)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)

        self.assertTrue('team' in responseData)
        teamData = responseData['team']

        # Now I check all the things
        # Starting with the team username
        self.assertTrue(fullTeamMatch(teamModel, teamData))

    def test_get_team_many(self):
        """
        Trying to get a single team out of like twenty or something
        but then it tries to get like every team anyways
        """
        player = CustomUserFactory()
        teamModels = []

        numPlayerOne = 10
        numPlayerTwo = 10

        for i in range(0, numPlayerOne):
            teamModels.append(TeamFactory(teamCaptain=player))
        for i in range(0, numPlayerTwo):
            teamModels.append(TeamFactory(teammate=player))

        client = APIClient()
        client.force_authenticate(user=player)
        for teamModel in teamModels:
            url = reverse('team_detail', kwargs={'teamId': teamModel.id})
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            responseData = json.loads(response.content)

            self.assertTrue('team' in responseData)
            teamData = responseData['team']

            # Now I check all the things
            # Starting with the team username
            self.assertTrue(fullTeamMatch(teamModel, teamData))

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': 0})
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
