from django.test import TestCase

from apps.my_auth.models import CustomUser

from ..models import Litter
from ..serializers import LitterSerializer


class LitterSerializerTests(TestCase):
    def test_model_fields(self):
        """Serializer data matches the Litter object for each field."""
        user = CustomUser.objects.create_user('test@gmail.com',
                                              password='pass4test')
        litterModel = Litter(typeOfLitter='IND', amount=50, user=user)
        serialized = LitterSerializer(litterModel)
        sData = serialized.data
        
        fields = ['typeOfLitter', 'amount', 'timeCollected']

        for field in fields:
            self.assertEqual(sData[field], getattr(litterModel, field))

    def test_model_fields_saved(self):
        """Serializer data matches the Litter object for each field."""
        user = CustomUser.objects.create_user('test@gmail.com',
                                              password='pass4test')
        litterModel = Litter(typeOfLitter='IND', amount=50, user=user)
        litterModel.save()
        serialized = LitterSerializer(litterModel)
        sData = serialized.data

        self.assertEqual(len(sData['id']), 8)

        fields = ['typeOfLitter', 'amount']

        for field in fields:
            self.assertEqual(sData[field], getattr(litterModel, field))
