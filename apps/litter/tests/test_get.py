import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import CustomUserFactory, LitterFactory


class Test_My_Litter_GET_Detail(TestCase):
    def test_get_litter_one_piece(self):
        """
        Trying to get a single piece of litter.
        """

        user = CustomUserFactory()
        inLitter = LitterFactory(user=user)

        client = APIClient()
        url = reverse('litter-detail', kwargs={'litterId': inLitter.id})
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['typeOfLitter'], inLitter.typeOfLitter)
        self.assertEqual(responseData['amount'], inLitter.amount)
        self.assertTrue(responseData['timeCollected'] is not None)
        self.assertEqual(len(responseData['id']), 8)

    def test_get_same_litter_twice(self):
        """
        Trying to get the same piece of litter twice.
        """
        user = CustomUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        litter = LitterFactory(user=user)
        url = reverse('litter-detail', kwargs={'litterId': litter.id})

        for i in range(0, 2):
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
            self.assertEqual(responseData['amount'], litter.amount)
            self.assertTrue(responseData['timeCollected'] is not None)
            self.assertEqual(len(responseData['id']), 8)

    def test_get_same_litter_many_times(self):
        """
        Trying to get all the litter a person has logged many times.
        Which is just one piece of litter
        """
        user = CustomUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        litter = LitterFactory(user=user)
        url = reverse('litter-detail', kwargs={'litterId': litter.id})

        for i in range(0, 100):
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
            self.assertEqual(responseData['amount'], litter.amount)
            self.assertTrue(responseData['timeCollected'] is not None)
            self.assertEqual(len(responseData['id']), 8)

    def test_get_two_litters(self):
        """
        Trying to get all the litter a person has logged.
        Which is two this time!
        """
        user = CustomUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        for i in range(0, 2):
            litter = LitterFactory(user=user)
            url = reverse('litter-detail', kwargs={'litterId': litter.id})
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
            self.assertEqual(responseData['amount'], litter.amount)
            self.assertTrue(responseData['timeCollected'] is not None)
            self.assertEqual(len(responseData['id']), 8)


    def test_get_many_litters(self):
        """
        Trying to get all the litter a person has logged.
        Which is a bunch in this case.
        """
        user = CustomUserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        for i in range(0, 100):
            litter = LitterFactory(user=user)
            url = reverse('litter-detail', kwargs={'litterId': litter.id})
            response = client.get(url)
            responseData = json.loads(response.content)

            self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
            self.assertEqual(responseData['amount'], litter.amount)
            self.assertTrue(responseData['timeCollected'] is not None)
            self.assertEqual(len(responseData['id']), 8)

    def test_get_wrong_litter(self):
        """
        Trying to get a litter at a bs litter id.
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('litter-detail', kwargs={'litterId': 0})
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['errors']['litterId'],
                         'Litter id not found: 0')

    def test_get_litter_not_yours(self):
        """
        Trying to get litter that isn't theirs
        """
        user1 = CustomUserFactory(email='user1')
        user2 = CustomUserFactory(email='user2')
        litter = LitterFactory(user=user2)

        client = APIClient()
        client.force_authenticate(user=user1)
        url = reverse('litter-detail', kwargs={'litterId': litter.id})
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData['errors']['litterId'],
                         'Litter id not found: ' + str(litter.id))

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


class Test_My_Litter_GET_List(TestCase):
    def test_get_litter_one_piece(self):
        """
        Trying to get all the litter a person has logged.
        """

        user = CustomUserFactory()
        litter = LitterFactory(user=user)

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), 1)
        self.assertEqual(responseData[0]['typeOfLitter'], litter.typeOfLitter)
        self.assertEqual(responseData[0]['amount'], litter.amount)
        self.assertTrue(responseData[0]['timeCollected'] is not None)
        self.assertEqual(len(responseData[0]['id']), 8)

    def test_get_litter_two_pieces(self):
        """
        Trying to get all the litter a person has logged.
        """

        user = CustomUserFactory()
        litter1 = LitterFactory(user=user)
        litter2 = LitterFactory(user=user)

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), 2)
        self.assertEqual(responseData[0]['typeOfLitter'], litter1.typeOfLitter)
        self.assertEqual(responseData[0]['amount'], litter1.amount)
        self.assertTrue(responseData[0]['timeCollected'] is not None)
        self.assertEqual(len(responseData[0]['id']), 8)
        self.assertEqual(responseData[1]['typeOfLitter'], litter2.typeOfLitter)
        self.assertEqual(responseData[1]['amount'], litter2.amount)
        self.assertTrue(responseData[1]['timeCollected'] is not None)
        self.assertEqual(len(responseData[1]['id']), 8)

    def test_get_litter_many_pieces(self):
        """
        Trying to get all the litter a person has logged. But a lot.
        """
        user = CustomUserFactory()
        litters = []
        for i in range(0, 100):
            litters.append(LitterFactory(user=user))

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), 100)
        for i in range(0, 100):
            self.assertEqual(responseData[i]['typeOfLitter'],
                             litters[i].typeOfLitter)
            self.assertEqual(responseData[i]['amount'], litters[i].amount)
            self.assertTrue(responseData[i]['timeCollected'] is not None)
            self.assertEqual(len(responseData[i]['id']), 8)

    def test_get_litter_no_pieces(self):
        """
        Trying to get all the litter a person has logged which is none.
        """
        user = CustomUserFactory()

        client = APIClient()
        url = reverse('litter-list')
        client.force_authenticate(user=user)
        response = client.get(url)
        responseData = json.loads(response.content)

        self.assertEqual(responseData, [])

    def test_no_authentication(self):
        """
        Trying to get all the litter without any user auth
        """
        client = APIClient()
        url = reverse('litter-list')
        response = client.get(url)

        self.assertEqual(response.status_code, 401)
