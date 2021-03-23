from django.test import TestCase

from apps.my_auth.models import CustomUser


class CustomUserModelTests(TestCase):
    def test_model_fields(self):
        """Super simple info in is info out."""

        email = 'test@gmail.com'
        username = 'username'
        user = CustomUser.objects.create_user(email=email,
                                              username=username,
                                              password='pass4test')

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
