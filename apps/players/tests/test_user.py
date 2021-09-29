from django.urls import reverse
from rest_framework.test import APIClient

from .checkers import BasicUserTesting
from .factories import PlayerFactory


class Test_Get_User_Data(BasicUserTesting):

    def test_get_user_data_other_user(self):
        """Testing retriving a regular user's data from a different user."""
        userModel = PlayerFactory()
        authModel = PlayerFactory()

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': userModel.uuid})
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
        userModel = PlayerFactory()

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': userModel.uuid})
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
        userModel = PlayerFactory()

        client = APIClient()
        url = reverse('PlayerList')
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

    def test_get_user_data_incorrect_uuid(self):
        """Testing retriving a player with an incorrect uuid."""
        userModel = PlayerFactory()

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': '00000000-0000-0000-0000-000000000000'})
        client.force_authenticate(user=userModel)
        response = client.get(url)

        self.assertResponse404(response)


class Test_Edit_User_Data(BasicUserTesting):

    def test_edit_username(self):
        """Testing changing my username."""
        authModel = PlayerFactory()

        data = {'username': 'newUsername'}

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': authModel.uuid})
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
        authModel = PlayerFactory()

        data = {'username': authModel.username}

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': authModel.uuid})
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
        authModel = PlayerFactory()
        otherModel = PlayerFactory()

        data = {'username': otherModel.username}

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': authModel.uuid})
        client.force_authenticate(user=authModel)
        response = client.patch(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'username': ["Username is not available."]}
        self.assertEqual(correctResponse, responseData)

    def test_edit_other_users_username(self):
        """Testing changing somebody else's username."""
        authModel = PlayerFactory()
        otherModel = PlayerFactory()

        data = {'username': 'newUsername'}

        client = APIClient()
        url = reverse('PlayerDetail', kwargs={'uuid': otherModel.uuid})
        client.force_authenticate(user=authModel)
        response = client.patch(url, data, format='json')

        self.assertResponse400(response)
        responseData = self.loadJSONSafely(response)
        correctResponse = {'non_field_errors': ["Can't edit a user that isn't you."]}
        self.assertEqual(correctResponse, responseData)
