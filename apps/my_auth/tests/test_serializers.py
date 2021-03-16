from django.test import TestCase

from ..models import CustomUser
from ..serializers import CustomUserSerializer
from ..factories import CustomUserFactory


class CustomUserSerializerTests(TestCase):
    def test_model_fields(self):
        """Serializer data matches the Point object for each field."""
        userModel = CustomUserFactory()
        serialized = CustomUserSerializer(userModel)
        sData = serialized.data
        
        fields = ['username', 'email']
        for field in fields:
            self.assertEqual(sData[field], getattr(userModel, field))

    def test_model_fields_multiple(self):
        """Serializer data matches the Point object for each field."""
        userModels = []
        for i in range(0, 10):
            userModels.append(CustomUserFactory())
        serialized = CustomUserSerializer(userModels, many=True)
        sData = serialized.data
        
        for i in range(0, 10):
            fields = ['username', 'email']
            for field in fields:
                self.assertEqual(sData[i][field], getattr(userModels[i], field))
