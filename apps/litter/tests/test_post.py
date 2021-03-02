import datetime
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import CustomUserFactory, LitterFactory


class Test_My_Litter_POST(TestCase):
    def test_one_post(self):
        """
        Testing one simple post
        """

        user = CustomUserFactory()
        litter = LitterFactory(user=user)
        data = {'typeOfLitter': litter.typeOfLitter,
                'amount': litter.amount,
                'timeCollected': datetime.datetime.now()}

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
        self.assertEqual(responseData['amount'], litter.amount)
        self.assertTrue(responseData['timeCollected'] is not None)
        self.assertTrue(responseData['id'] is not None)

    def test_two_posts(self):
        """
        Testing two posts
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)

        for i in range(0, 2):
            litter = LitterFactory(user=user)
            data = {'typeOfLitter': litter.typeOfLitter,
                    'amount': litter.amount,
                    'timeCollected': datetime.datetime.now()}
            response = client.post(url, data, format='json')
            responseData = json.loads(response.content)

            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
            self.assertEqual(responseData['amount'], litter.amount)
            self.assertTrue(responseData['timeCollected'] is not None)
            self.assertTrue(responseData['id'] is not None)

    def test_many_posts(self):
        """
        Testing many posts
        """

        user = CustomUserFactory()

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)

        for i in range(0, 100):
            litter = LitterFactory(user=user)
            data = {'typeOfLitter': litter.typeOfLitter,
                    'amount': litter.amount,
                    'timeCollected': datetime.datetime.now()}
            response = client.post(url, data, format='json')
            responseData = json.loads(response.content)

            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
            self.assertEqual(responseData['amount'], litter.amount)
            self.assertTrue(responseData['timeCollected'] is not None)
            self.assertTrue(responseData['id'] is not None)

    def test_no_posts(self):
        """
        Testing a post with no data
        """

        user = CustomUserFactory()

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)
        response = client.post(url, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['amount'][0], 'This field is required.')

    def test_no_authentication(self):
        """
        Trying to get POST litter without any user auth
        """
        client = APIClient()
        url = reverse('litter-list')
        response = client.post(url, format='json')

        self.assertEqual(response.status_code, 401)
