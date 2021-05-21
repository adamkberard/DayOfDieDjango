import json

from django.test import TestCase


class Friend_Testing_Helpers(TestCase):
    def checkFriendMatch(self, data, check_against_data):
        fields = [
            'uuid', 'status', 'team_name', 'wins', 'losses', 'league'
        ]
        self.assertEqual(len(data), len(check_against_data))

        for field in fields:
            self.assertTrue(field in data)
            self.assertEqual(data.get(field), check_against_data.get(field))

            # Check the two users seperately
            self.assertTrue('team_captain' in data)
            self.assertTrue('teammate' in data)

            team_captain = data.get('team_captain')
            teammate = data.get('teammate')

            self.assertEqual(team_captain['username'],
                             check_against_data.get('team_captain')['username'])
            self.assertEqual(team_captain['uuid'],
                             check_against_data.get('team_captain')['uuid'])
            self.assertEqual(teammate['username'],
                             check_against_data.get('teammate')['username'])
            self.assertEqual(teammate['uuid'],
                             check_against_data.get('teammate')['uuid'])

    def checkFriend(self, response, check_against_data):
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        self.checkFriendMatch(responseData, check_against_data)

    def checkFriends(self, response, check_against_data):
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)

        self.assertEqual(len(responseData), len(check_against_data))

        for i in range(len(responseData)):
            self.checkFriendMatch(responseData[i], check_against_data[i])
