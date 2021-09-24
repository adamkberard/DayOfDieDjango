from apps.my_auth.serializers import CustomUserReadSerializer
from apps.my_auth.tests.factories import CustomUserFactory
from apps.teams.models import Team

from ..serializers import TeamSerializer
from .checkers import TeamTesting
from .factories import TeamFactory


class Test_Team_Serializers(TeamTesting):

    def test_team_serializer(self):
        """Testing the team serializer."""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        teamship = Team(
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
            'uuid': str(teamship.uuid)
        }
        self.assertEqual(correctData, TeamSerializer(teamship).data)

    def test_team_serializer_from_factory(self):
        """Testing the team serializer."""
        teamship = TeamFactory()
        correctData = {
            'team_captain': CustomUserReadSerializer(teamship.team_captain).data,
            'teammate': CustomUserReadSerializer(teamship.teammate).data,
            'status': teamship.status,
            'wins': 0,
            'losses': 0,
            'uuid': str(teamship.uuid)
        }
        self.assertEqual(correctData, TeamSerializer(teamship).data)
