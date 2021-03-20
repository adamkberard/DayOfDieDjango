# import json
#
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
#
# from apps.my_auth.factories import CustomUserFactory
#
# from ..factories import GameFactory, PointFactory
#
#
# class Test_My_Litter_PUT(TestCase):
#     def test_easy_successful_put_type(self):
#         """
#         Testing a simple put
#         """
#
#         user = CustomUserFactory()
#         amount = 40
#         amountChange = 20
#         litter = LitterFactory(user=user, amount=amount)
#
#         data = {'typeOfLitter': litter.typeOfLitter,
#                 'amount': litter.amount + amountChange,
#                 'timeCollected': litter.timeCollected}
#
#         client = APIClient()
#         url = reverse('litter-detail', kwargs={'litterId': litter.id})
#         client.force_authenticate(user=user)
#         response = client.put(url, data, format='json')
#         responseData = json.loads(response.content)
#
#         self.assertEqual(responseData['typeOfLitter'], litter.typeOfLitter)
#         self.assertEqual(responseData['amount'], litter.amount +amountChange)
#         self.assertTrue(responseData['timeCollected'] is not None)
#         self.assertTrue(responseData['id'] is not None)
#
#     def test_put_litter_not_owned(self):
#         """
#         Testing a simple put but on an object not owned by the putter
#         """
#
#         user1 = CustomUserFactory(email='user1@gmail.com')
#         user2 = CustomUserFactory(email='user2@gmail.com')
#         amount = 40
#         amountChange = 20
#         litter = LitterFactory(user=user1, amount=amount)
#
#         data = {'typeOfLitter': litter.typeOfLitter,
#                 'amount': litter.amount + amountChange,
#                 'timeCollected': litter.timeCollected}
#
#         client = APIClient()
#         url = reverse('litter-detail', kwargs={'litterId': litter.id})
#         client.force_authenticate(user=user2)
#         response = client.put(url, data, format='json')
#         responseData = json.loads(response.content)
#
#         self.assertEqual(responseData['errors']['litterId'],
#                          'Litter id not found: ' + str(litter.id))
#
#     def test_bad_litter_id(self):
#         """
#         Testing a simple put with no litter id
#         """
#
#         user = CustomUserFactory()
#         litter = LitterFactory(user=user)
#
#         data = {'typeOfLitter': litter.typeOfLitter,
#                 'amount': litter.amount,
#                 'timeCollected': litter.timeCollected}
#
#         client = APIClient()
#         url = reverse('litter-detail', kwargs={'litterId': 0})
#         client.force_authenticate(user=user)
#         response = client.put(url, data, format='json')
#         responseData = json.loads(response.content)
#
#         self.assertEqual(responseData['errors']['litterId'],
#                          'Litter id not found: 0')
#
#     def test_no_authentication(self):
#         """
#         Trying to PUT litter without any user auth
#         """
#         client = APIClient()
#         user = CustomUserFactory()
#         litter = LitterFactory(user=user)
#         url = reverse('litter-detail', kwargs={'litterId': litter.id})
#         response = client.put(url, format='json')
#
#         self.assertEqual(response.status_code, 401)
