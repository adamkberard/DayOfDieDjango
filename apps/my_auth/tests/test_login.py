import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import CustomUser


class Test_Login_View(TestCase):

    def test_correct_login(self):
        """Testing a legitimate login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'test@gmail.com', 'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertTrue(responseData['token'] is not None)
        self.assertTrue(responseData['username'] is not None)

    def test_incorrect_user_login(self):
        """Testing an incorrect email/username login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'gmail@gmail.com', 'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(responseData['error'], 'Email or password wrong.')

    def test_incorrect_pass_login(self):
        """Testing an incorrect password login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'test@gmail.com', 'password': 'incorrectPass'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(responseData['error'], 'Email or password wrong.')

    def test_incorrect_user_and_pass_login(self):
        """Testing an incorrect password login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'gmail@gmail.com', 'password': 'incorrectPass'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(responseData['error'], 'Email or password wrong.')

    def test_login_no_email(self):
        data = {'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responseData['email'][0],
                         'This field is required.')

    def test_login_no_pass(self):
        data = {'email': 'test@gmail.com'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responseData['password'][0],
                         'This field is required.')

    def test_login_no_user_or_pass(self):
        data = {}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(responseData['email'][0], 'This field is required.')
        self.assertEqual(responseData['password'][0],
                         'This field is required.')
