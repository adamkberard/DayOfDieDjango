import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.friends.models import Friend
from apps.my_auth.tests.factories import CustomUserFactory

from ..serializers import FriendSerializer
from .checkers import Friend_Testing_Helpers
from .factories import FriendFactory


class Test_Friend_URL_Params(TestCase):
    helper = Friend_Testing_Helpers()

    def test_friend_request_no_params(self):
        """Testing a bad friend request with no params."""
        friendModel = FriendFactory()
        data = {}

        client = APIClient()
        client.force_authenticate(user=friendModel.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('teammate' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['teammate'], ['This field is required.'])

    def test_friend_request_no_teammate_but_status(self):
        """Testing a bad friend request with only the status param."""
        friendModel = FriendFactory()
        data = {'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendModel.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('teammate' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['teammate'], ['This field is required.'])

    def test_friend_request_invalid_status(self):
        """Testing a bad friend request with only the status param that is invalid."""
        friendModel = FriendFactory()
        data = {'teammate': friendModel.teammate.username,
                'status': 'invalid'}

        client = APIClient()
        client.force_authenticate(user=friendModel.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('status' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['status'], ['"invalid" is not a valid choice.'])


class Test_Create_Nonexistent_Friend(TestCase):
    helper = Friend_Testing_Helpers()

    def test_nonexistent_friend_block(self):
        """Testing a friend request that is a block on a nonexistent friendship."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(requester, requested)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, requester)
        self.assertEqual(friendModel.teammate, requested)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nonexistent_friend_nothing(self):
        """Testing a friend request that is a nothing on a nonexistent friendship.
           This is not allowed."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('non_field_errors' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['non_field_errors'],
                         ['Cannot create a "Nothing" friend request.'])

    def test_nonexistent_friend_pending(self):
        """Testing a friend request that is a pending on a nonexistent friendship."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(requester, requested)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, requester)
        self.assertEqual(friendModel.teammate, requested)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nonexistent_friend_accept(self):
        """Testing a friend request that is an accept on a nonexistent friendship."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(requester, requested)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, requester)
        self.assertEqual(friendModel.teammate, requested)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)


class Test_Create_Existent_Friend_Blocked(TestCase):
    helper = Friend_Testing_Helpers()

    def test_blocking_existing_blocked_friend_as_team_captain(self):
        """Testing re-blocking an existing blocked friend request as
           the team captain aka the blocker."""
        friendship = FriendFactory(status=Friend.STATUS_BLOCKED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_blocked_friend_as_team_captain(self):
        """Testing changing an existing blocked friend request to nothing
           as the team captain aka the blocker."""
        friendship = FriendFactory(status=Friend.STATUS_BLOCKED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_NOTHING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_pendinging_an_existing_blocked_friend_as_team_captain(self):
        """Testing changing an existing blocked friend request to pending as
           the team captain aka the blocker. This is not allowed."""
        friendship = FriendFactory(status=Friend.STATUS_BLOCKED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        # The response we want
        self.assertEqual(response.status_code, 400)
        # Make sure error exists
        self.assertTrue('non_field_errors' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['non_field_errors'],
                         ['This action is not allowed when blocking.'])

    def test_accepting_an_existing_blocked_friend_as_team_captain(self):
        """Testing changing an existing blocked friend request to accepted as
           the team captain aka the blocker. This is not allowed."""
        friendship = FriendFactory(status=Friend.STATUS_BLOCKED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        # The response we want
        self.assertEqual(response.status_code, 400)
        # Make sure error exists
        self.assertTrue('non_field_errors' in responseData)
        # Make sure it's the correct error
        self.assertEqual(responseData['non_field_errors'],
                         ['This action is not allowed when blocking.'])

    def test_doing_everything_to_existing_blocked_friend_as_teammate(self):
        """Testing doing anything to an existing blocked friend request
           as the teammate aka the blockee."""
        friendship = FriendFactory(status=Friend.STATUS_BLOCKED)

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')

        for status in [item[0] for item in Friend.STATUS_CHOICES]:
            data = {'teammate': friendship.team_captain.username, 'status': status}

            response = client.post(url, data, format='json')
            responseData = json.loads(response.content)

            # The response we want
            self.assertEqual(response.status_code, 400)
            # Make sure error exists
            self.assertTrue('non_field_errors' in responseData)
            # Make sure it's the correct error
            self.assertEqual(responseData['non_field_errors'],
                             ['This action is not allowed when blocked.'])


class Test_Create_Existent_Friend_Nothing(TestCase):
    helper = Friend_Testing_Helpers()

    def test_blocking_an_existing_nothing_friend_as_team_captain(self):
        """Testing blocking an existing nothing friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_blocking_an_existing_nothing_friend_as_teammate(self):
        """Testing blocking an existing nothing friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, friendship.teammate)
        self.assertEqual(friendModel.teammate, friendship.team_captain)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_nothing_friend_as_team_captain(self):
        """Testing nothinging an existing nothing friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_nothing_friend_as_teammate(self):
        """Testing nothinging an existing nothing friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_pendinging_an_existing_nothing_friend_as_team_captain(self):
        """Testing pendinging an existing nothing friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_pendinging_an_existing_nothing_friend_as_teammate(self):
        """Testing pendinging an existing nothing friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, friendship.teammate)
        self.assertEqual(friendModel.teammate, friendship.team_captain)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_accepting_an_existing_nothing_friend_as_team_captain(self):
        """Testing accepting an existing nothing friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_accepting_an_existing_nothing_friend_as_teammate(self):
        """Testing accepting an existing nothing friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_NOTHING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, friendship.teammate)
        self.assertEqual(friendModel.teammate, friendship.team_captain)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)


class Test_Create_Existent_Friend_Pending(TestCase):
    helper = Friend_Testing_Helpers()

    def test_blocking_an_existing_pending_friend_as_team_captain(self):
        """Testing blocking an existing pending friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_blocking_an_existing_pending_friend_as_teammate(self):
        """Testing blocking an existing pending friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, friendship.teammate)
        self.assertEqual(friendModel.teammate, friendship.team_captain)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_pending_friend_as_team_captain(self):
        """Testing nothinging an existing pending friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_NOTHING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_pending_friend_as_teammate(self):
        """Testing nothinging an existing pending friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_NOTHING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_pendinging_an_existing_pending_friend_as_team_captain(self):
        """Testing pendinging an existing pending friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_pendinging_an_existing_pending_friend_as_teammate(self):
        """Testing pendinging an existing pending friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_accepting_an_existing_pending_friend_as_team_captain(self):
        """Testing accepting an existing pending friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_PENDING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_accepting_an_existing_pending_friend_as_teammate(self):
        """Testing accepting an existing pending friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_PENDING)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_ACCEPTED)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)


class Test_Create_Existent_Friend_Accepted(TestCase):
    helper = Friend_Testing_Helpers()

    def test_blocking_an_existing_accepted_friend_as_team_captain(self):
        """Testing blocking an existing accepted friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_blocking_an_existing_accepted_friend_as_teammate(self):
        """Testing blocking an existing accepted friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_BLOCKED)
        self.assertEqual(friendModel.team_captain, friendship.teammate)
        self.assertEqual(friendModel.teammate, friendship.team_captain)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_accepted_friend_as_team_captain(self):
        """Testing nothinging an existing accepted friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_NOTHING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_nothinging_an_existing_accepted_friend_as_teammate(self):
        """Testing nothinging an existing accepted friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel.status, Friend.STATUS_NOTHING)
        self.assertEqual(friendModel.team_captain, friendship.team_captain)
        self.assertEqual(friendModel.teammate, friendship.teammate)
        self.assertEqual(friendModel.wins, 0)
        self.assertEqual(friendModel.losses, 0)
        self.assertEqual(friendModel.league, Friend.LEAGUE_UNRANKED)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_pendinging_an_existing_accepted_friend_as_team_captain(self):
        """Testing pendinging an existing accepted friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('non_field_errors' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['non_field_errors'],
                         ['Cannot go from accepted frieend request to pending.'])

    def test_pendinging_an_existing_accepted_friend_as_teammate(self):
        """Testing pendinging an existing accepted friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # Make sure things went wrong first
        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        # Make sure error exists
        self.assertTrue('non_field_errors' in responseData)

        # Make sure it's the correct error
        self.assertEqual(responseData['non_field_errors'],
                         ['Cannot go from accepted frieend request to pending.'])

    def test_accepting_an_existing_accepted_friend_as_team_captain(self):
        """Testing accepting an existing accepted friend request as the team captain."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.teammate.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.team_captain)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)

    def test_accepting_an_existing_accepted_friend_as_teammate(self):
        """Testing accepting an existing accepted friend request as the teammate."""
        friendship = FriendFactory(status=Friend.STATUS_ACCEPTED)
        data = {'teammate': friendship.team_captain.username, 'status': Friend.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=friendship.teammate)
        url = reverse('friend_request_create')
        response = client.post(url, data, format='json')

        # The response we want
        friendModel = Friend.objects.get_friendship(friendship.team_captain, friendship.teammate)

        # Make sure friend model is okay
        self.assertEqual(friendModel, friendship)

        # Make the dict to compare return to
        check_against_friend = FriendSerializer(friendModel).data

        # Check return
        self.helper.checkFriend(response, check_against_friend)
