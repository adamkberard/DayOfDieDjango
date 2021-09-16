from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.tests.factories import CustomUserFactory
from apps.teams.models import Team

from ..serializers import TeamSerializer
from .checkers import TeamTesting
from .factories import TeamFactory


class Test_Team_URL_Params(TeamTesting):

    def test_team_request_no_params(self):
        """Testing a bad team request with no params."""
        teamModel = TeamFactory()
        data = {}

        client = APIClient()
        client.force_authenticate(user=teamModel.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'teammate': ['This field is required.'],
            'status': ['This field is required.']
        }
        self.assertEqual(correctResponse, responseData)

    def test_team_request_no_teammate_(self):
        """Testing a bad team request with only the status param."""
        teamModel = TeamFactory()
        data = {'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamModel.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'teammate': ['This field is required.']}
        self.assertEqual(correctResponse, responseData)

    def test_team_request_invalid_status(self):
        """Testing a bad team request with only the status param that is invalid."""
        teamModel = TeamFactory()
        data = {'teammate': teamModel.teammate.username,
                'status': 'invalid'}

        client = APIClient()
        client.force_authenticate(user=teamModel.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'status': ['"invalid" is not a valid choice.']}
        self.assertEqual(correctResponse, responseData)


class Test_Create_Nonexistent_Team(TeamTesting):

    def test_nonexistent_team_block(self):
        """Testing a team request that is a block on a nonexistent teamship."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(requester, requested)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, requester)
        self.assertEqual(teamModel.teammate, requested)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nonexistent_team_nothing(self):
        """Testing a team request that is a nothing on a nonexistent teamship.
           This is not allowed."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'non_field_errors': ['Cannot create a "Nothing" team request.']}
        self.assertEqual(correctResponse, responseData)

    def test_nonexistent_team_pending(self):
        """Testing a team request that is a pending on a nonexistent teamship."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(requester, requested)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, requester)
        self.assertEqual(teamModel.teammate, requested)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nonexistent_team_accept(self):
        """Testing a team request that is an accept on a nonexistent teamship."""
        requester = CustomUserFactory()
        requested = CustomUserFactory()
        data = {'teammate': requested.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(requester, requested)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, requester)
        self.assertEqual(teamModel.teammate, requested)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)


class Test_Create_Existent_Team_Blocked(TeamTesting):

    def test_blocking_existing_blocked_team_as_team_captain(self):
        """Testing re-blocking an existing blocked team request as
           the team captain aka the blocker."""
        teamship = TeamFactory(status=Team.STATUS_BLOCKED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)

        self.assertEqual(teamModel, teamship)
        correctResponse = TeamSerializer(teamModel).data

        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_blocked_team_as_team_captain(self):
        """Testing changing an existing blocked team request to nothing
           as the team captain aka the blocker."""
        teamship = TeamFactory(status=Team.STATUS_BLOCKED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_NOTHING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_blocked_team_as_team_captain(self):
        """Testing changing an existing blocked team request to pending as
           the team captain aka the blocker. This is not allowed."""
        teamship = TeamFactory(status=Team.STATUS_BLOCKED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        # The response we want
        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'non_field_errors': ['This action is not allowed when blocking.']}
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_blocked_team_as_team_captain(self):
        """Testing changing an existing blocked team request to accepted as
           the team captain aka the blocker. This is not allowed."""
        teamship = TeamFactory(status=Team.STATUS_BLOCKED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        # The response we want
        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'non_field_errors': ['This action is not allowed when blocking.']}
        self.assertEqual(correctResponse, responseData)

    def test_doing_everything_to_existing_blocked_team_as_teammate(self):
        """Testing doing anything to an existing blocked team request
           as the teammate aka the blockee."""
        teamship = TeamFactory(status=Team.STATUS_BLOCKED)

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')

        for status in [item[0] for item in Team.STATUS_CHOICES]:
            data = {'teammate': teamship.team_captain.username, 'status': status}

            response = client.post(url, data, format='json')

            # The response we want
            self.assertResponse400(response)
            responseData = self.loadJSONSafely(response)
            correctResponse = {'non_field_errors': ['This action is not allowed when blocked.']}
            self.assertEqual(correctResponse, responseData)


class Test_Create_Existent_Team_Nothing(TeamTesting):

    def test_blocking_an_existing_nothing_team_as_team_captain(self):
        """Testing blocking an existing nothing team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_blocking_an_existing_nothing_team_as_teammate(self):
        """Testing blocking an existing nothing team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, teamship.teammate)
        self.assertEqual(teamModel.teammate, teamship.team_captain)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_nothing_team_as_team_captain(self):
        """Testing nothinging an existing nothing team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel, teamship)

        correctResponse = TeamSerializer(teamModel).data
        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_nothing_team_as_teammate(self):
        """Testing nothinging an existing nothing team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel, teamship)

        correctResponse = TeamSerializer(teamModel).data
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_nothing_team_as_team_captain(self):
        """Testing pendinging an existing nothing team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_nothing_team_as_teammate(self):
        """Testing pendinging an existing nothing team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, teamship.teammate)
        self.assertEqual(teamModel.teammate, teamship.team_captain)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_nothing_team_as_team_captain(self):
        """Testing accepting an existing nothing team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_nothing_team_as_teammate(self):
        """Testing accepting an existing nothing team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_NOTHING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, teamship.teammate)
        self.assertEqual(teamModel.teammate, teamship.team_captain)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)


class Test_Create_Existent_Team_Pending(TeamTesting):

    def test_blocking_an_existing_pending_team_as_team_captain(self):
        """Testing blocking an existing pending team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0

        # Check return
        self.assertEqual(correctResponse, responseData)

    def test_blocking_an_existing_pending_team_as_teammate(self):
        """Testing blocking an existing pending team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, teamship.teammate)
        self.assertEqual(teamModel.teammate, teamship.team_captain)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_pending_team_as_team_captain(self):
        """Testing nothinging an existing pending team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_NOTHING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_pending_team_as_teammate(self):
        """Testing nothinging an existing pending team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_NOTHING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_pending_team_as_team_captain(self):
        """Testing pendinging an existing pending team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel, teamship)

        correctResponse = TeamSerializer(teamModel).data
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_pending_team_as_teammate(self):
        """Testing pendinging an existing pending team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel, teamship)

        correctResponse = TeamSerializer(teamModel).data
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_pending_team_as_team_captain(self):
        """Testing accepting an existing pending team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_PENDING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_pending_team_as_teammate(self):
        """Testing accepting an existing pending team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_PENDING)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_ACCEPTED)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)


class Test_Create_Existent_Team_Accepted(TeamTesting):

    def test_blocking_an_existing_accepted_team_as_team_captain(self):
        """Testing blocking an existing accepted team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_blocking_an_existing_accepted_team_as_teammate(self):
        """Testing blocking an existing accepted team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_BLOCKED}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_BLOCKED)
        self.assertEqual(teamModel.team_captain, teamship.teammate)
        self.assertEqual(teamModel.teammate, teamship.team_captain)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_accepted_team_as_team_captain(self):
        """Testing nothinging an existing accepted team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_NOTHING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_nothinging_an_existing_accepted_team_as_teammate(self):
        """Testing nothinging an existing accepted team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_NOTHING}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel.status, Team.STATUS_NOTHING)
        self.assertEqual(teamModel.team_captain, teamship.team_captain)
        self.assertEqual(teamModel.teammate, teamship.teammate)

        correctResponse = TeamSerializer(teamModel).data
        correctResponse['wins'] = 0
        correctResponse['losses'] = 0
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_accepted_team_as_team_captain(self):
        """Testing pendinging an existing accepted team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)

        correctResponse = {
            'non_field_errors': ['Cannot go from accepted team request to pending.']
        }
        self.assertEqual(correctResponse, responseData)

    def test_pendinging_an_existing_accepted_team_as_teammate(self):
        """Testing pendinging an existing accepted team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_PENDING}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)

        correctResponse = {
            'non_field_errors': ['Cannot go from accepted team request to pending.']
        }
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_accepted_team_as_team_captain(self):
        """Testing accepting an existing accepted team request as the team captain."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.teammate.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.team_captain)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel, teamship)

        correctResponse = TeamSerializer(teamModel).data
        self.assertEqual(correctResponse, responseData)

    def test_accepting_an_existing_accepted_team_as_teammate(self):
        """Testing accepting an existing accepted team request as the teammate."""
        teamship = TeamFactory(status=Team.STATUS_ACCEPTED)
        data = {'teammate': teamship.team_captain.username, 'status': Team.STATUS_ACCEPTED}

        client = APIClient()
        client.force_authenticate(user=teamship.teammate)
        url = reverse('team_generic')
        response = client.post(url, data, format='json')

        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        teamModel = Team.objects.get_team(teamship.team_captain, teamship.teammate)
        self.assertEqual(teamModel, teamship)

        correctResponse = TeamSerializer(teamModel).data
        self.assertEqual(correctResponse, responseData)
