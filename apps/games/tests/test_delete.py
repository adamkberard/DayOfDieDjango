import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory


class Test_My_Litter_DELETE(TestCase):
    def test_easy_successful_delete_type(self):
        """
        Testing a simple delete
        """

        user = CustomUserFactory()
        litter = LitterFactory(user=user)

        client = APIClient()
        url = reverse('litter-detail', kwargs={'litterId': litter.id})
        client.force_authenticate(user=user)
        response = client.delete(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['status'], 'okay')

    def test_delete_litter_not_owned(self):
        """
        Testing a simple delete but on an object not owned by the deleter
        """

        user1 = CustomUserFactory(email='user1')
        user2 = CustomUserFactory(email='user2')
        litter = LitterFactory(user=user1)

        client = APIClient()
        url = reverse('litter-detail', kwargs={'litterId': litter.id})
        client.force_authenticate(user=user2)
        response = client.delete(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['errors']['litterId'],
                         'Litter id not found: ' + str(litter.id))

    def test_bad_litter_id(self):
        """
        Testing a simple delete with no litter id
        """

        user = CustomUserFactory()

        client = APIClient()
        url = reverse('litter-detail', kwargs={'litterId': 0})
        client.force_authenticate(user=user)
        response = client.delete(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['errors']['litterId'],
                         'Litter id not found: 0')

    def test_no_authentication(self):
        """
        Trying to PUT litter without any user auth
        """
        client = APIClient()
        user = CustomUserFactory()
        litter = LitterFactory(user=user)
        url = reverse('litter-detail', kwargs={'litterId': litter.id})
        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, 401)
