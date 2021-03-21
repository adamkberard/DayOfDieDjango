import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import FriendFactory
from ..models import Friend


class Test_Friend_DELETE(TestCase):
    def test_simple_delete(self):
        """
        Testing a simple delete of a friend
        """
        friendModel = FriendFactory()

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=friendModel.friendOne)
        response = client.delete(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['status'], 'okay')
        self.assertEqual(Friend.objects.filter(id=friendModel.id).count(), 0)

    def test_delete_friend_not_in(self):
        """
        Testing a simple delete but on a friend the user wasn't in
        """
        friendModel = FriendFactory()
        playerThree = CustomUserFactory()

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=playerThree)
        response = client.delete(url)
        responseData = json.loads(response.content)

        errStr = 'Friend id not found: '
        self.assertTrue(responseData['error'].startswith(errStr))

    def test_bad_litter_id(self):
        """
        Testing a simple delete with no litter id
        """
        friendModel = FriendFactory()
        playerThree = CustomUserFactory()

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=playerThree)
        response = client.delete(url)
        responseData = json.loads(response.content)

        errStr = 'Friend id not found: '
        self.assertTrue(responseData['error'].startswith(errStr))

    def test_no_authentication(self):
        """
        Trying to PUT litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': 0})
        response = client.delete(url)

        self.assertEqual(response.status_code, 401)
