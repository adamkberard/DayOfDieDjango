from django.test import TestCase

from apps.my_auth.models import CustomUser

from ..models import Litter


class LitterModelTests(TestCase):
    def test_model_fields(self):
        """Super simple info in is info out."""
        user = CustomUser.objects.create_user('test@gmail.com',
                                              password='pass4test')
        typeOfLitter = 'IND'
        amount = 50

        litterModel = Litter(typeOfLitter=typeOfLitter,
                             amount=amount,
                             user=user)

        self.assertEqual(litterModel.typeOfLitter, typeOfLitter)
        self.assertEqual(litterModel.amount, amount)

    def test_model_fields_with_saved(self):
        """Super simple info in is info out now with saved model."""
        user = CustomUser.objects.create_user('test@gmail.com',
                                              password='pass4test')
        typeOfLitter = 'IND'
        amount = 50

        litterModel = Litter(typeOfLitter=typeOfLitter,
                             amount=amount,
                             user=user)
        litterModel.save()

        self.assertEqual(litterModel.typeOfLitter, typeOfLitter)
        self.assertEqual(litterModel.amount, amount)
