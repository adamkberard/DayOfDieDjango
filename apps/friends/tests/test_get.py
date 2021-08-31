from django.urls import reverse
from rest_framework.test import APIClient

from apps.friends.models import Friend
from apps.my_auth.tests.factories import CustomUserFactory
from apps.my_auth.serializers import CustomUserReadSerializer

from ..serializers import FriendSerializer
from .checkers import FriendTesting
from .factories import FriendFactory



class Test_Friend_GET(FriendTesting):

    def test_friend_get_no_friends(self):
        """Testing a friend request get with no friends."""
        user = CustomUserFactory()

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('friend_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = []
        self.assertEqual(correctResponse, responseData)

    def test_friend_get_one_friend_as_team_captain(self):
        """Testing a friend request get with one friend."""
        friendship = FriendFactory()

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [
            {
                'uuid': str(friendship.uuid),
                'status': friendship.status,
                'team_captain': CustomUserReadSerializer(friendship.team_captain).data,
                'teammate': CustomUserReadSerializer(friendship.teammate).data,
                'wins': 0,
                'losses': 0
            }
        ]
        self.assertEqual(correctResponse, responseData)

    def test_friend_get_one_friend_as_teammate(self):
        """Testing a friend request get with one friend."""
        friendship = FriendFactory()

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [
            {
                'uuid': str(friendship.uuid),
                'status': friendship.status,
                'team_captain': CustomUserReadSerializer(friendship.team_captain).data,
                'teammate': CustomUserReadSerializer(friendship.teammate).data,
                'wins': 0,
                'losses': 0
            }
        ]
        self.assertEqual(correctResponse, responseData)

    def test_getting_many_friends(self):
        numFriends = 5
        correctResponse = []
        user = CustomUserFactory()

        for _ in range(numFriends):
            friendship = FriendFactory(team_captain=user)
            correctResponse.append({
                'uuid': str(friendship.uuid),
                'status': friendship.status,
                'team_captain': CustomUserReadSerializer(friendship.team_captain).data,
                'teammate': CustomUserReadSerializer(friendship.teammate).data,
                'wins': 0,
                'losses': 0
            })

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('friend_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        self.assertEqual(correctResponse, responseData)

    def test_friend_get_one_friend_as_team_captain_with_other_friends(self):
        """Testing a friend request get with one friend."""
        friendship = FriendFactory()
        FriendFactory.create_batch(5)

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_generic')
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [
            {
                'uuid': str(friendship.uuid),
                'status': friendship.status,
                'team_captain': CustomUserReadSerializer(friendship.team_captain).data,
                'teammate': CustomUserReadSerializer(friendship.teammate).data,
                'wins': 0,
                'losses': 0
            }
        ]
        self.assertEqual(correctResponse, responseData)
