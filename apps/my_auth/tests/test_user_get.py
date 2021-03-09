import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.litter.tests.factories import CustomUserFactory, LitterFactory


class Test_User_GET(TestCase):
    def test_getting_user_data(self):
        """
        Trying to access user data
        """

        user = CustomUserFactory()
        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['username'], user.username)
        self.assertEqual(responseData['email'], user.email)
        self.assertEqual(responseData['id'], user.id)

    def test_get_user_data_twice(self):
        """
        Trying to access user data twice
        """
        user = CustomUserFactory()
        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)

        # Check Twice
        for i in range(0, 2):
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertEqual(responseData['username'], user.username)
            self.assertEqual(responseData['email'], user.email)
            self.assertEqual(responseData['id'], user.id)

    def test_get_user_data_many_times(self):
        """
        Trying to access user data a lot
        """
        user = CustomUserFactory()
        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)

        # Check Twice
        for i in range(0, 100):
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertEqual(responseData['username'], user.username)
            self.assertEqual(responseData['email'], user.email)
            self.assertEqual(responseData['id'], user.id)

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        user = CustomUserFactory()
        litter = LitterFactory(user=user)
        url = reverse('litter-detail', kwargs={'litterId': litter.id})
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
