import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import CustomUser


class Test_Register_View(TestCase):
    def test_correct_register(self):
        """Testing a registration login."""
        data = {'email': 'test10@gmail.com', 'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        self.assertTrue('token' in responseData)
        self.assertTrue('username' in responseData)

        self.assertTrue(responseData['token'] is not None)
        self.assertTrue(responseData['username'] is not None)

    def test_incorrect_user_register(self):
        """Testing a registration login where the username is taken."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'test@gmail.com', 'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 401)
        responseData = json.loads(response.content)

        estr = 'Could not create an account with those credentials.'
        self.assertEqual(responseData['errors'], [estr])

    def test_register_no_email(self):
        data = {'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'][0],
                         'This field is required.')

    def test_register_no_pass(self):
        data = {'email': 'test@gmail.com'}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['password'][0],
                         'This field is required.')

    def test_register_no_user_or_pass(self):
        data = {}

        client = APIClient()
        url = reverse('my_register')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'][0], 'This field is required.')
        self.assertEqual(responseData['password'][0],
                         'This field is required.')
