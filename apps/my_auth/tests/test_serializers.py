from apps.players.models import Player
from apps.players.serializers import PlayerReadSerializer

from .checkers import AuthTesting
from apps.players.tests.factories import PlayerFactory


class Test_User_Serializer(AuthTesting):
    def test_correct_login_no_data(self):
        """Testing a legitimate login."""
        userModel = Player.objects.create(
            username='test_username',
            email='test@email.com',
        )
        correctData = {
            'username': 'test_username',
            'wins': 0,
            'losses': 0,
            'uuid': str(userModel.uuid)
        }
        self.assertEqual(correctData, PlayerReadSerializer(userModel).data)

    def test_correct_login_no_data_from_factory(self):
        """Testing a legitimate login."""
        userModel = PlayerFactory()
        correctData = {
            'username': userModel.username,
            'wins': 0,
            'losses': 0,
            'uuid': str(userModel.uuid)
        }
        self.assertEqual(correctData, PlayerReadSerializer(userModel).data)
