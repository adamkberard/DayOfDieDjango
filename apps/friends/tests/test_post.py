import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import FriendFactory
from ..serializers import FriendSerializer
from .comparers import checkFriendMatch


class Test_Friend_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        friendModel = FriendFactory.build(requester=requester,
                                          requested=requested)
        friendModelData = FriendSerializer(friendModel).data

        data = {'friend': requested.username}

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=requester)
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        avoid = ['id', 'timeRequested', 'timeRespondedTo']
        friendMatched = checkFriendMatch(responseData, friendModelData,
                                         toAvoid=avoid)
        self.assertEqual('valid', friendMatched)

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
