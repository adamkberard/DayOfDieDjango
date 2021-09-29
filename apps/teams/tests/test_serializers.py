from apps.players.tests.factories import PlayerFactory
from apps.players.serializers import PlayerReadSerializer
from apps.teams.models import Team

from ..serializers import TeamSerializer
from .checkers import TeamTesting
from .factories import TeamFactory


class Test_Team_Serializers(TeamTesting):

    def test_team_serializer(self):
        """Testing the team serializer."""
        user1 = PlayerFactory()
        user2 = PlayerFactory()
        teamship = Team(
            team_captain=user1,
            teammate=user2,
            status='pd'
        )
        correctData = {
            'team_captain': PlayerReadSerializer(user1).data,
            'teammate': PlayerReadSerializer(user2).data,
            'team_name': None,
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
            'team_captain': PlayerReadSerializer(teamship.team_captain).data,
            'teammate': PlayerReadSerializer(teamship.teammate).data,
            'team_name': None,
            'status': teamship.status,
            'wins': 0,
            'losses': 0,
            'uuid': str(teamship.uuid)
        }
        self.assertEqual(correctData, TeamSerializer(teamship).data)
