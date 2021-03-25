import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import TeamFactory
from ..serializers import TeamSerializer
from .comparers import checkTeamMatch


class Test_Team_GET(TestCase):
    def test_get_teams_single(self):
        """
        Trying to get all the teams a person has. It comes as a list of
        teams. They only have one team in this case.
        """
        player = CustomUserFactory()
        teamModel = TeamFactory(teamCaptain=player)
        teamModelData = TeamSerializer(teamModel).data

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('teams' in responseData)
        self.assertEqual(len(responseData['teams']), 1)
        teamSet = responseData['teams'][0]

        teamMatched = checkTeamMatch(teamSet, teamModelData,
                                     both=False)
        self.assertEqual('valid', teamMatched)

    def test_get_teams_many(self):
        """
        Trying to get all the teams a person has. It comes as a list of
        teams. They only have one team in this case.
        """
        player = CustomUserFactory()
        teamModels = []
        teamModelDatas = []

        numRequester = 10
        numRequested = 10
        totalTeams = numRequester + numRequested

        for i in range(0, numRequester):
            tempModel = TeamFactory(teamCaptain=player)
            teamModels.append(tempModel)
            teamModelDatas.append(TeamSerializer(tempModel).data)
        for i in range(0, numRequested):
            tempModel = TeamFactory(teammate=player)
            teamModels.append(tempModel)
            teamModelDatas.append(TeamSerializer(tempModel).data)

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('teams' in responseData)
        self.assertEqual(len(responseData['teams']), totalTeams)
        for i in range(0, totalTeams):
            teamSet = responseData['teams'][i]
            teamModelData = teamModelDatas[i]
            teamMatched = checkTeamMatch(teamSet, teamModelData,
                                         both=False)
            self.assertEqual('valid', teamMatched)

    def test_get_no_teams(self):
        """
        Trying to get all the teams a person has logged which is none.
        """
        player = CustomUserFactory()

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('teams' in responseData)
        self.assertEqual(len(responseData['teams']), 0)

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
        player = CustomUserFactory()
        teamModel = TeamFactory(teamCaptain=player)
        teamModelData = TeamSerializer(teamModel).data

        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': teamModel.id})
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        teamMatched = checkTeamMatch(responseData, teamModelData,
                                     both=True)
        self.assertEqual('valid', teamMatched)

    def test_get_team_many(self):
        """
        Trying to get a single team out of like twenty or something
        but then it tries to get like every team anyways
        """
        player = CustomUserFactory()
        teamModels = []
        teamModelDatas = []

        numRequester = 10
        numRequested = 10
        totalTeams = numRequester + numRequested

        for i in range(0, numRequester):
            tempModel = TeamFactory(teamCaptain=player)
            teamModels.append(tempModel)
            teamModelDatas.append(TeamSerializer(tempModel).data)
        for i in range(0, numRequested):
            tempModel = TeamFactory(teammate=player)
            teamModels.append(tempModel)
            teamModelDatas.append(TeamSerializer(tempModel).data)

        client = APIClient()
        client.force_authenticate(user=player)

        for i in range(0, totalTeams):
            teamModel = teamModels[i]
            teamModelData = teamModelDatas[i]

            url = reverse('team_detail', kwargs={'teamId': teamModel.id})
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            responseData = json.loads(response.content)
            self.assertEqual(len(responseData), 1)

            teamMatched = checkTeamMatch(responseData, teamModelData,
                                         both=True)
            self.assertEqual('valid', teamMatched)

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('team_detail', kwargs={'teamId': 0})
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
