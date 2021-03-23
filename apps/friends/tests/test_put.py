import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from tools.ids_encoder import decode_id

from ..factories import FriendFactory

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

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        friendModel.status = friendModel.ACCEPTED

        self.assertTrue('friend' in responseData)
        friendData = responseData['friend']

        # Gotta make sure the friend id didn't change cuz that would
        # be annoying
        self.assertTrue('id' in friendData)
        self.assertEqual(friendModel.id, decode_id(friendData['id']))

        # First I'll check the date times
        dateFStr = '%Y-%m-%d %H:%M:%S'
        self.assertTrue('timeRequested' in friendData)
        self.assertEqual(friendData['timeRequested'],
                         friendModel.timeRequested.strftime(dateFStr))
        self.assertTrue('timeRespondedTo' in friendData)
        self.assertEqual(friendData['timeRespondedTo'],
                         friendModel.timeRespondedTo.strftime(dateFStr))

        # Then I'll check the players
        self.assertTrue('requester' in friendData)
        self.assertEqual(friendModel.requester.username,
                         friendData['requester'])
        self.assertTrue('requested' in friendData)
        self.assertEqual(friendModel.requested.username,
                         friendData['requested'])

        # Finally make sure we actually changed the status
        self.assertTrue('status' in friendData)
        self.assertTrue(friendModel.status, friendData['status'])

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

        # Now that we have the data, I can change the model without affecting
        # anything. It just makes testing easier
        friendModel.status = friendModel.DENIED

        self.assertTrue('friend' in responseData)
        friendData = responseData['friend']

        # Gotta make sure the friend id didn't change cuz that would
        # be annoying
        self.assertTrue('id' in friendData)
        self.assertEqual(friendModel.id, decode_id(friendData['id']))

        # First I'll check the date times
        dateFStr = '%Y-%m-%d %H:%M:%S'
        self.assertTrue('timeRequested' in friendData)
        self.assertEqual(friendData['timeRequested'],
                         friendModel.timeRequested.strftime(dateFStr))
        self.assertTrue('timeRespondedTo' in friendData)
        self.assertEqual(friendData['timeRespondedTo'],
                         friendModel.timeRespondedTo.strftime(dateFStr))

        # Then I'll check the players
        self.assertTrue('requester' in friendData)
        self.assertEqual(friendModel.requester.username,
                         friendData['requester'])
        self.assertTrue('requested' in friendData)
        self.assertEqual(friendModel.requested.username,
                         friendData['requested'])

        # Finally make sure we actually changed the status
        self.assertTrue('status' in friendData)
        self.assertTrue(friendModel.status, friendData['status'])

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
