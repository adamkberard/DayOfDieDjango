from django.urls import reverse
from rest_framework.test import APIClient

from apps.friends.models import Friend
from apps.my_auth.tests.factories import CustomUserFactory
from apps.my_auth.serializers import CustomUserReadSerializer

from .checkers import FriendTesting
from .factories import FriendFactory
from ..serializers import FriendSerializer



class Test_Friend_Serializers(FriendTesting):

    def test_friend_serializer(self):
        """Testing the friend serializer."""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        friendship = Friend(
            team_captain=user1,
            teammate=user2,
            status='pd'
        )
        correctData = {
            'team_captain': CustomUserReadSerializer(user1).data,
            'teammate': CustomUserReadSerializer(user2).data,
            'status': 'pd',
            'wins': 0,
            'losses': 0,
            'uuid': str(friendship.uuid)
        }
        self.assertEqual(correctData, FriendSerializer(friendship).data)

    def test_friend_serializer_from_factory(self):
        """Testing the friend serializer."""
        friendship = FriendFactory()
        correctData = {
            'team_captain': CustomUserReadSerializer(friendship.team_captain).data,
            'teammate': CustomUserReadSerializer(friendship.teammate).data,
            'status': friendship.status,
            'wins': 0,
            'losses': 0,
            'uuid': str(friendship.uuid)
        }
        self.assertEqual(correctData, FriendSerializer(friendship).data)
