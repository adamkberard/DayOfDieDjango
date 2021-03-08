import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.litter.tests.factories import CustomUserFactory, LitterFactory


class Test_User_POST(TestCase):
    def test_updating_email(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        newEmail = 'tempUsername@gmail.com'
        data = {'email': newEmail}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], newEmail)
        self.assertEqual(responseData['id'], user.id)
        self.assertEqual(responseData['username'], user.username)

    # Can't update id, it just wont do it. No error it just doesn't work
    def test_updating_id(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        newId = 10
        data = {'id': newId}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], user.email)
        self.assertEqual(responseData['id'], user.id)
        self.assertEqual(responseData['username'], user.username)

    def test_updating_username(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        newUsername = 'tempUsername'
        data = {'username': newUsername}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], user.email)
        self.assertEqual(responseData['id'], user.id)
        self.assertEqual(responseData['username'], newUsername)

    # Can't update id, it just wont do it. No error it just doesn't work
    def test_updating_email_and_id(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        newEmail = 'tempUsername@gmail.com'
        newId = 10
        data = {'email': newEmail,
                'id': newId}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], newEmail)
        self.assertEqual(responseData['id'], user.id)
        self.assertEqual(responseData['username'], user.username)

    def test_updating_email_and_username(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        newEmail = 'tempUsername@gmail.com'
        newUsername = 'tempUsername'
        data = {'email': newEmail,
                'username': newUsername}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], newEmail)
        self.assertEqual(responseData['id'], user.id)
        self.assertEqual(responseData['username'], newUsername)

    # Can't update id, it just wont do it. No error it just doesn't work
    def test_updating_id_and_username(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        newUsername = 'tempUsername'
        newId = 10
        data = {'username': newUsername,
                'id': newId}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['email'], user.email)
        self.assertEqual(responseData['id'], user.id)
        self.assertEqual(responseData['username'], newUsername)

    # Can't update id, it just wont do it. No error it just doesn't work
    def test_updating_email_and_username_and_id(self):
        """
        Trying to update user data
        ID cannot be updated
        """
        user = CustomUserFactory()
        newEmail = 'tempUsername@gmail.com'
        newUsername = 'tempUsername'
        newId = 10
        data = {'email': newEmail,
                'username': newUsername,
                'id': newId}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
        responseData = json.loads(response.content)

        self.assertEqual(responseData['username'], newUsername)
        self.assertEqual(responseData['email'], newEmail)
        self.assertEqual(responseData['id'], user.id)

    # This is essentially just a weird get
    # Might wanna disallow this, but honestly idk why I would bother
    def test_updating_nothing(self):
        """
        Trying to update user data
        """
        user = CustomUserFactory()
        data = {}

        client = APIClient()
        url = reverse('my_username')
        client.force_authenticate(user=user)
        response = client.post(url, data, format='json')
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
