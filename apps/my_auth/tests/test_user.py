from django.urls import reverse
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
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'username': userModel.username,
            'uuid': str(userModel.uuid),
            'wins': 0,
            'losses': 0
        }
        self.assertEqual(correctResponse, responseData)

    def test_get_user_data_same_user(self):
        """Testing retriving a user's own data."""
        userModel = CustomUserFactory()

        client = APIClient()
        url = 'http://testserver/users/' + userModel.username + '/'
        client.force_authenticate(user=userModel)
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'username': userModel.username,
            'uuid': str(userModel.uuid),
            'wins': 0,
            'losses': 0
        }
        self.assertEqual(correctResponse, responseData)

    def test_get_user_data_many(self):
        """Testing retriving all the users which is only one."""
        userModel = CustomUserFactory()

        client = APIClient()
        url = reverse('user_view')
        client.force_authenticate(user=userModel)
        response = client.get(url)

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = [{
            'username': userModel.username,
            'uuid': str(userModel.uuid),
            'wins': 0,
            'losses': 0
        }]
        self.assertEqual(correctResponse, responseData)

    def test_get_user_data_incorrect_username(self):
        """Testing retriving a regular user's data from a different user."""
        userModel = CustomUserFactory()

        client = APIClient()
        url = 'http://testserver/users/' + 'badUsername' + '/'
        client.force_authenticate(user=userModel)
        response = client.get(url)

        self.assertResponse404(response)


class Test_Edit_User_Data(BasicUserTesting):

    def test_edit_username(self):
        """Testing changing my username."""
        authModel = CustomUserFactory()

        data = {'username': 'newUsername'}

        client = APIClient()
        url = 'http://testserver/users/' + authModel.username + '/'
        client.force_authenticate(user=authModel)
        response = client.patch(url, data, format='json')

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'username': 'newUsername',
            'uuid': str(authModel.uuid),
            'wins': 0,
            'losses': 0
        }
        self.assertEqual(correctResponse, responseData)

    def test_updating_username_to_current_username(self):
        """Testing changing my username to what it already is."""
        authModel = CustomUserFactory()

        data = {'username': authModel.username}

        client = APIClient()
        url = 'http://testserver/users/' + authModel.username + '/'
        client.force_authenticate(user=authModel)
        response = client.patch(url, data, format='json')

        self.assertResponse200(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {
            'username': authModel.username,
            'uuid': str(authModel.uuid),
            'wins': 0,
            'losses': 0
        }
        self.assertEqual(correctResponse, responseData)

    def test_edit_username_already_existing(self):
        """Testing changing my username to something that already exists."""
        authModel = CustomUserFactory()
        otherModel = CustomUserFactory()

        data = {'username': otherModel.username}

        client = APIClient()
        url = 'http://testserver/users/' + authModel.username + '/'
        client.force_authenticate(user=authModel)
        response = client.patch(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'username': ["Username is not available."]}
        self.assertEqual(correctResponse, responseData)

    def test_edit_other_users_username(self):
        """Testing changing somebody else's username."""
        authModel = CustomUserFactory()
        otherModel = CustomUserFactory()

        data = {'username': 'newUsername'}

        client = APIClient()
        url = 'http://testserver/users/' + otherModel.username + '/'
        client.force_authenticate(user=authModel)
        response = client.patch(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'non_field_errors': ["Can't edit a user that isn't you."]}
        self.assertEqual(correctResponse, responseData)
