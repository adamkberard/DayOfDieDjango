import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..factories import FriendFactory
from ..serializers import FriendSerializer
from .comparers import checkFriendMatch

# Change player and make sure points change too
# Make sure the id doesn't change for friends after edits


class Test_Friend_PUT(TestCase):
    def test_put_accept_friend_as_requested(self):
        """
        Testing one simple put of accepting a friend request
        """
        friendModel = FriendFactory()

        data = {'status': 'accept'}

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=friendModel.requested)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        friendModel.status = friendModel.ACCEPTED
        friendModelData = FriendSerializer(friendModel).data

        avoid = ['id', 'timeRequested', 'timeRespondedTo']
        friendMatched = checkFriendMatch(responseData, friendModelData,
                                         toAvoid=avoid)
        self.assertEqual('valid', friendMatched)

    def test_put_accept_friend_as_requester(self):
        """
        Testing one simple put of accepting a friend request
        """
        friendModel = FriendFactory()

        data = {'status': 'accept'}

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=friendModel.requester)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        estr = 'Cannot accept a friend request as the requester.'
        self.assertEqual(responseData['errors'], [estr])

    def test_put_denied_friend_as_requsted(self):
        """
        Testing one simple put of denying a friend request as requested
        """
        friendModel = FriendFactory()

        data = {'status': 'deny'}

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=friendModel.requested)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        friendModel.status = friendModel.DENIED
        friendModelData = FriendSerializer(friendModel).data

        avoid = ['id', 'timeRequested', 'timeRespondedTo']
        friendMatched = checkFriendMatch(responseData, friendModelData,
                                         toAvoid=avoid)
        self.assertEqual('valid', friendMatched)

    def test_put_denied_friend_as_requester(self):
        """
        Testing one simple put of accepting a friend request
        """
        friendModel = FriendFactory()

        data = {'status': 'deny'}

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=friendModel.requester)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        estr = 'Cannot deny a friend request as the requester.'
        self.assertEqual(responseData['errors'], [estr])

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_list')
        response = client.put(url, format='json')

        self.assertEqual(response.status_code, 401)
