from apps.core.checker import BaseChecker


class AuthTesting(BaseChecker):

    def assertBasicUserEqual(self, data1, data2):
        fields = ['username', 'uuid']
        self.assertDictEqual(data1, data2, fields)

    def assertFullUserEqual(self, data1, data2):
        fields = ['email', 'username', 'uuid', 'token']
        self.assertDictEqual(data1, data2, fields)

    def assertAllUsersEqual(self, data, check_against_data):
        self.assertEqual(len(data), len(check_against_data))
        # Need to make sure they're the same order someday

        for username in check_against_data:
            try:
                data.remove(username)
            except ValueError:
                self.fail('All user list didnt match.')

    def assertLoginResponseSuccess(self, response, check_against_data):
        self.assertResponse201(response)
        responseData = self.loadJSONSafely(response)
        self.assertLoginDictEqual(responseData, check_against_data)

    def assertLoginDictEqual(self, data, check_against_data):
        # I do some stuff early
        from apps.friends.tests.checkers import FriendTesting
        from apps.games.tests.checkers import GameTesting
        gameTester = GameTesting()
        friendTester = FriendTesting()

        self.assertFullUserEqual(data.get('user'), check_against_data.get('user'))

        # Now check the games
        gameTester.assertGamesEqual(data.get('games'), check_against_data.get('games'))

        # Now check the friends
        friendTester.assertFriendsEqual(data.get('friends'), check_against_data.get('friends'))

        # Now make sure all the usernames are here
        self.assertAllUsersEqual(data['all_users'], check_against_data['all_users'])
