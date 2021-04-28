import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import CustomUser
from ..serializers import CustomUserSerializer
from .comparers import checkLoginMatch


class Test_Login_View(TestCase):

    def test_correct_login(self):
        """Testing a legitimate login."""
        email = 'test@gmail.com'
        password = 'pass4test'
        myModel = CustomUser.objects.create_user(email, password)
        modelData = CustomUserSerializer(myModel).data
        data = {'email': email, 'password': password}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        matched = checkLoginMatch(responseData, modelData)
        self.assertEqual('valid', matched)

    def test_incorrect_user_login(self):
        """Testing an incorrect email/username login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'gmail@gmail.com', 'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 401)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        self.assertEqual(responseData['errors'], ['Email or password wrong.'])

    def test_incorrect_pass_login(self):
        """Testing an incorrect password login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'test@gmail.com', 'password': 'incorrectPass'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 401)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        self.assertEqual(responseData['errors'], ['Email or password wrong.'])

    def test_incorrect_user_and_pass_login(self):
        """Testing an incorrect password login."""
        CustomUser.objects.create_user('test@gmail.com', password='pass4test')
        data = {'email': 'gmail@gmail.com', 'password': 'incorrectPass'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 401)
        responseData = json.loads(response.content)

        self.assertTrue('errors' in responseData)
        self.assertEqual(responseData['errors'], ['Email or password wrong.'])

    def test_login_no_email(self):
        data = {'password': 'pass4test'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], ['This field is required.'])

    def test_login_no_pass(self):
        data = {'email': 'test@gmail.com'}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['password'],
                         ['This field is required.'])

    def test_login_no_user_or_pass(self):
        data = {}

        client = APIClient()
        url = reverse('my_login')
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], ['This field is required.'])
        self.assertEqual(responseData['password'],
                         ['This field is required.'])
