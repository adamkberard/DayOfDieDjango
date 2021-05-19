import json

from django.test import TestCase


class Auth_Testing_Helpers(TestCase):
    def checkUser(self, data, check_against_data):
        fields = ['email', 'username', 'uuid', 'token']

        for field in fields:
            self.assertTrue(field in data)
            self.assertEqual(data.get(field), check_against_data.get(field))

    def checkGames(self, data, check_against_data):
        fields = [
            'points', 'team_one', 'team_two', 'time_started', 'time_ended', 'uuid', 'type',
            'team_one_score', 'team_two_score', 'confirmed'
        ]

        self.assertEqual(len(data), len(check_against_data))
        for i in range(len(data)):
            for field in fields:
                self.assertTrue(field in data[i])
                self.assertEqual(data[i].get(field), check_against_data[i].get(field))

    def checkFriends(self, data, check_against_data):
        fields = [
            'uuid', 'status', 'team_name', 'wins', 'losses', 'league'
        ]

        self.assertEqual(len(data), len(check_against_data))
        for i in range(len(data)):
            for field in fields:
                self.assertTrue(field in data[i])
                self.assertEqual(data[i].get(field), check_against_data[i].get(field))

                # Check the two users seperately
                self.assertTrue('team_captain' in data[i])
                self.assertTrue('teammate' in data[i])

                team_captain = data[i].get('team_captain')
                teammate = data[i].get('teammate')

                self.assertEqual(team_captain['username'],
                                 check_against_data[i].get('team_captain')['username'])
                self.assertEqual(team_captain['uuid'],
                                 check_against_data[i].get('team_captain')['uuid'])
                self.assertEqual(teammate['username'],
                                 check_against_data[i].get('teammate')['username'])
                self.assertEqual(teammate['uuid'],
                                 check_against_data[i].get('teammate')['uuid'])

    def checkAllUsernames(self, data, check_against_data):
        self.assertEqual(len(data), len(check_against_data))
        # Need to make sure they're the same someday

        for username in check_against_data:
            try:
                data.remove(username)
            except ValueError:
                self.fail('Username list didnt match.')

    def checkLoginReturn(self, response, check_against_data):
        self.assertEqual(response.status_code, 201)
        responseData = json.loads(response.content)
        self.checkLoginFields(responseData)
        self.checkLoginData(responseData, check_against_data)

    def checkLoginFields(self, data):
        self.assertTrue('user' in data)
        self.assertTrue('games' in data)
        self.assertTrue('friends' in data)
        self.assertTrue('all_usernames' in data)

    def checkLoginData(self, data, check_against_data):
        self.checkUser(data['user'], check_against_data['user'])
        self.checkGames(data['games'], check_against_data['games'])
        self.checkFriends(data['friends'], check_against_data['friends'])
        self.checkAllUsernames(data['all_usernames'], check_against_data['all_usernames'])
