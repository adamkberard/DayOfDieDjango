import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory


class Test_Friend_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        requesterModel = CustomUserFactory()
        requestedModel = CustomUserFactory()

        data = {'friend': requestedModel.username}

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=requesterModel)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertTrue('friend' in responseData)
        friendData = responseData['friend']

        # First I'll check to make sure the dates exist
        self.assertTrue('timeRequested' in friendData)
        self.assertTrue('timeRespondedTo' in friendData)

        # Then I check the status
        self.assertEqual(friendData['status'], 'PD')

        # Then I'll check the friend
        self.assertEqual(friendData['requested'], requestedModel.username)

        # Then make sure we got an ID back
        self.assertTrue(len(friendData['id']) >= 8)

    def test_no_posts(self):
        """
        Testing a post with no data
        """

        user = CustomUserFactory()

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=user)
        response = client.post(url, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['friend'][0], 'This field is required.')

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
