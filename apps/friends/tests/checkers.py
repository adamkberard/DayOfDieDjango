from apps.core.checker import BaseChecker
from apps.my_auth.tests.checkers import AuthTesting


class FriendTesting(BaseChecker):

    def assertFriendEqual(self, data1, data2):
        userTester = AuthTesting()
        fields = [
            'uuid', 'status', 'team_name', 'wins', 'losses', 'league'
        ]
        self.assertDictEqual(data1, data2, fields)

        # Now we check the two users
        userTester.assertBasicUserEqual(data1.get('team_captain'), data2.get('team_captain'))
        userTester.assertBasicUserEqual(data1.get('teammate'), data2.get('teammate'))

    def assertFriendsEqual(self, data1, data2):
        self.assertEqual(len(data1), len(data2))

        for i in range(len(data1)):
            self.assertFriendEqual(data1[i], data2[i])

    def assertFriendResponseValid(self, response, check_against_data):
        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)

        self.assertFriendEqual(responseData, check_against_data)
