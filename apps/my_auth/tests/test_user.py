import json
from datetime import datetime, timedelta

import pytz
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .checkers import BasicUserTesting
from .factories import CustomUserFactory

class Test_Get_User_Data(BasicUserTesting):

    def test_get_user_data_other_user(self):
        """Testing retriving a regular user's data from a different user."""
        userModel = CustomUserFactory()
        authModel = CustomUserFactory()

        client = APIClient()
        url = 'http://testserver/users/' + userModel.username + '/'
        client.force_authenticate(user=authModel)
        self.response = client.get(url)

        self.check_against_data = {
            'username': userModel.username,
            'uuid': str(userModel.uuid),
            'wins': 0,
            'losses': 0
        }
        self.assertResponse200()
        self.assertResponseEqual()

    def test_get_user_data_same_user(self):
        """Testing retriving a regular user's data from a different user."""
        userModel = CustomUserFactory()

        client = APIClient()
        url = 'http://testserver/users/' + userModel.username + '/'
        client.force_authenticate(user=userModel)
        self.response = client.get(url)

        self.check_against_data = {
            'username': userModel.username,
            'uuid': str(userModel.uuid),
            'wins': 0,
            'losses': 0
        }
        
        self.assertResponse200()
        self.assertResponseEqual()

    def test_get_user_data_many(self):
        """Testing retriving all the users which is only one."""
        userModel = CustomUserFactory()

        client = APIClient()
        url = reverse('user_view')
        client.force_authenticate(user=userModel)
        self.response = client.get(url)

        self.check_against_data = [{
            'username': userModel.username,
            'uuid': str(userModel.uuid),
            'wins': 0,
            'losses': 0
        }]
        self.assertResponse200()
        self.assertResponseEqual()

    def test_get_user_data_incorrect_username(self):
        """Testing retriving a regular user's data from a different user."""
        userModel = CustomUserFactory()

        client = APIClient()
        url = 'http://testserver/users/' + 'badUsername' + '/'
        client.force_authenticate(user=userModel)
        self.response = client.get(url)

        self.assertResponse404()

class Test_Edit_User_Data(BasicUserTesting):

    def test_edit_username(self):
        """Testing changing my username."""
        authModel = CustomUserFactory()

        data = {'username' : 'newUsername'}

        client = APIClient()
        url = 'http://testserver/users/' + authModel.username + '/'
        client.force_authenticate(user=authModel)
        self.response = client.put(url, data, format='json')

        self.check_against_data = {
            'username': 'newUsername',
            'uuid': str(authModel.uuid),
            'wins': 0,
            'losses': 0
        }
        self.assertResponse200()
        self.assertResponseEqual()

    def test_edit_other_users_username(self):
        """Testing changing somebody else's username."""
        authModel = CustomUserFactory()
        otherModel = CustomUserFactory()

        data = {'username' : 'newUsername'}

        client = APIClient()
        url = 'http://testserver/users/' + otherModel.username + '/'
        client.force_authenticate(user=authModel)
        self.response = client.put(url, data, format='json')

        self.assertResponse400()
        self.loadJSONSafely()
        self.check_against_data = {'non_field_errors': ["Can't edit a user that isn't you."]}
        self.assertResponseEqual()