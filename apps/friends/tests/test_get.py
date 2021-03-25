import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import FriendFactory
from ..serializers import FriendSerializer
from .comparers import checkFriendMatch


class Test_Friend_GET(TestCase):
    def test_get_friends_single(self):
        """
        Trying to get all the friends a person has. It comes as a list of
        friends. They only have one friend in this case.
        """
        player = CustomUserFactory()
        friendModel = FriendFactory(requester=player)
        friendModelData = FriendSerializer(friendModel).data

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('friends' in responseData)
        self.assertEqual(len(responseData['friends']), 1)
        friendSet = responseData['friends'][0]

        friendMatched = checkFriendMatch(friendSet, friendModelData,
                                         both=False)
        self.assertEqual('valid', friendMatched)

    def test_get_friends_many(self):
        """
        Trying to get all the friends a person has. It comes as a list of
        friends. They only have one friend in this case.
        """
        player = CustomUserFactory()
        friendModels = []
        friendModelDatas = []

        numRequester = 10
        numRequested = 10
        totalFriends = numRequester + numRequested

        for i in range(0, numRequester):
            tempModel = FriendFactory(requester=player)
            friendModels.append(tempModel)
            friendModelDatas.append(FriendSerializer(tempModel).data)
        for i in range(0, numRequested):
            tempModel = FriendFactory(requested=player)
            friendModels.append(tempModel)
            friendModelDatas.append(FriendSerializer(tempModel).data)

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('friends' in responseData)
        self.assertEqual(len(responseData['friends']), totalFriends)
        for i in range(0, totalFriends):
            friendSet = responseData['friends'][i]
            friendModelData = friendModelDatas[i]
            friendMatched = checkFriendMatch(friendSet, friendModelData,
                                             both=False)
            self.assertEqual('valid', friendMatched)

    def test_get_no_friends(self):
        """
        Trying to get all the friends a person has logged which is none.
        """
        player = CustomUserFactory()

        client = APIClient()
        url = reverse('friend_list')
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        self.assertTrue('friends' in responseData)
        self.assertEqual(len(responseData['friends']), 0)

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
        player = CustomUserFactory()
        friendModel = FriendFactory(requester=player)
        friendModelData = FriendSerializer(friendModel).data

        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
        client.force_authenticate(user=player)
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEqual(len(responseData), 1)

        friendMatched = checkFriendMatch(responseData, friendModelData,
                                         both=True)
        self.assertEqual('valid', friendMatched)

    def test_get_friend_many(self):
        """
        Trying to get a single friend out of like twenty or something
        but then it tries to get like every friend anyways
        """
        player = CustomUserFactory()
        friendModels = []
        friendModelDatas = []

        numRequester = 10
        numRequested = 10
        totalFriends = numRequester + numRequested

        for i in range(0, numRequester):
            tempModel = FriendFactory(requester=player)
            friendModels.append(tempModel)
            friendModelDatas.append(FriendSerializer(tempModel).data)
        for i in range(0, numRequested):
            tempModel = FriendFactory(requested=player)
            friendModels.append(tempModel)
            friendModelDatas.append(FriendSerializer(tempModel).data)

        client = APIClient()
        client.force_authenticate(user=player)

        for i in range(0, totalFriends):
            friendModel = friendModels[i]
            friendModelData = friendModelDatas[i]

            url = reverse('friend_detail', kwargs={'friendId': friendModel.id})
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            responseData = json.loads(response.content)
            self.assertEqual(len(responseData), 1)

            friendMatched = checkFriendMatch(responseData, friendModelData,
                                             both=True)
            self.assertEqual('valid', friendMatched)

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('friend_detail', kwargs={'friendId': 0})
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
