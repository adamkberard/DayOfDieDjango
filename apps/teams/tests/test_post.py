import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory


class Test_Team_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        teamCaptainModel = CustomUserFactory()
        teammateModel = CustomUserFactory()

        data = {'teammate': teammateModel.username}

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=teamCaptainModel)
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        self.assertTrue('team' in responseData)
        teamData = responseData['team']

        # First I'll check to make sure the dates exist
        self.assertTrue('timeRequested' in teamData)
        self.assertTrue('timeRespondedTo' in teamData)

        # Then I check the status
        self.assertEqual(teamData['status'], 'PD')

        # Then I'll check the team
        self.assertEqual(teamData['teammate'], teammateModel.username)

        # Then make sure we got an ID back
        self.assertTrue(len(teamData['id']) >= 8)

    def test_no_posts(self):
        """
        Testing a post with no data
        """

        user = CustomUserFactory()

        client = APIClient()
        url = reverse('team_list')
        client.force_authenticate(user=user)
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['teammate'], ['This field is required.'])

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('team_list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
