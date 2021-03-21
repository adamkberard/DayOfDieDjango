import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory
from tools.helperFunctions.testHelperFuncs import friendsMatch, fullFriendMatch

from ..factories import FriendFactory


class Test_Friend_GET(TestCase):
    def test_get_friends_single(self):
        """
        Trying to get all the friends a person has. It comes as a list of
        friends. They only have one friend in this case.
        """
        player = CustomUserFactory()
        friendModels = []

        numPlayerOne = 1
        numPlayerTwo = 0
        totalFriends = numPlayerOne + numPlayerTwo

        for i in range(0, numPlayerOne):
            friendModels.append(FriendFactory(friendOne=player))
        for i in range(0, numPlayerTwo):
            friendModels.append(FriendFactory(friendTwo=player))

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=player)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertTrue('friends' in responseData)
        friendsData = responseData['friends']

        # Make sure the number of friends is one
        self.assertEqual(len(friendsData), totalFriends)

        # Now I check all the things
        # Starting with the friend username
        self.assertTrue(friendsMatch(friendModels, friendsData))

    def test_get_friends_many(self):
        """
        Trying to get all the friends a person has. It comes as a list of
        friends. They only have one friend in this case.
        """
        player = CustomUserFactory()
        friendModels = []

        numPlayerOne = 10
        numPlayerTwo = 10
        totalFriends = numPlayerOne + numPlayerTwo

        for i in range(0, numPlayerOne):
            friendModels.append(FriendFactory(friendOne=player))
        for i in range(0, numPlayerTwo):
            friendModels.append(FriendFactory(friendTwo=player))

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=player)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertTrue('friends' in responseData)
        friendsData = responseData['friends']

        # Make sure the number of friends is one
        self.assertEqual(len(friendsData), totalFriends)

        # Now I check all the things
        # Starting with the friend username
        self.assertTrue(friendsMatch(friendModels, friendsData))

    def test_get_no_friends(self):
        """
        Trying to get all the friends a person has logged which is none.
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['friends'], [])

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)


class Test_Friend_GET_Detail(TestCase):
    def test_get_friend(self):
        """
        Trying to get a single friend based on their id
        """
        friendModel = FriendFactory()

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=friendModel.friendOne)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertTrue('friend' in responseData)
        friendData = responseData['friend']

        # Now I check all the things
        # Starting with the friend username
        self.assertTrue(fullFriendMatch(friendModel, friendData))

    def test_get_friend_many(self):
        """
        Trying to get a single friend out of like twenty or something
        but then it tries to get like every friend anyways
        """
        player = CustomUserFactory()
        friendModels = []

        numPlayerOne = 10
        numPlayerTwo = 10

        for i in range(0, numPlayerOne):
            friendModels.append(FriendFactory(friendOne=player))
        for i in range(0, numPlayerTwo):
            friendModels.append(FriendFactory(friendTwo=player))

        client = APIClient()
        client.force_authenticate(user=player)
        for friendModel in friendModels:
            url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertTrue('friend' in responseData)
            friendData = responseData['friend']

            # Now I check all the things
            # Starting with the friend username
            self.assertTrue(fullFriendMatch(friendModel, friendData))

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': 0})
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
