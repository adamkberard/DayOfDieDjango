from ..models import CustomUser
from ..serializers import CustomUserReadSerializer
from .checkers import AuthTesting
from .factories import CustomUserFactory


class Test_User_Serializer(AuthTesting):
    def test_correct_login_no_data(self):
        """Testing a legitimate login."""
        userModel = CustomUser.objects.create(
            username='test_username',
            email='test@email.com',
        )
        correctData = {
            'username': 'test_username',
            'wins': 0,
            'losses': 0,
            'uuid': str(userModel.uuid)
        }
        self.assertEqual(correctData, CustomUserReadSerializer(userModel).data)

    def test_correct_login_no_data_from_factory(self):
        """Testing a legitimate login."""
        userModel = CustomUserFactory()
        correctData = {
            'username': userModel.username,
            'wins': 0,
            'losses': 0,
            'uuid': str(userModel.uuid)
        }
        self.assertEqual(correctData, CustomUserReadSerializer(userModel).data)
