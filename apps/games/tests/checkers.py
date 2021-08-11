from apps.core.checker import BaseChecker


class GameTesting(BaseChecker):
    def assertPointEqual(self, data1, data2):
        fields = [
            'points', 'team_one', 'team_two', 'time_started', 'time_ended', 'uuid',
            'team_one_score', 'team_two_score', 'confirmed'
        ]

        self.assertEqual(len(data1), len(data2))

        for field in fields:
            self.assertEqual(data1.get(field), data2.get(field))

    def assertGameEqual(self, data1, data2):
        fields = [
            'team_one', 'team_two', 'time_started', 'time_ended', 'uuid',
            'team_one_score', 'team_two_score', 'confirmed'
        ]

        self.assertEqual(len(data1), len(data2))

        for field in fields:
            self.assertEqual(data1.get(field), data2.get(field))

        self.assertTrue('points' in data1)
        self.assertTrue('points' in data2)

        points1 = data1.get('points')
        points2 = data2.get('points')

        # Now we check the points
        self.assertEqual(len(points1), len(points2))

        # If they have the same number of points but that's zero just return
        if len(data1.get('points')) == 0:
            return

        # Now I check each point and remove it from the other list. This ensures they have the
        # exact same amount of each point. There's gotta be a better way to do it, but that's
        # a later thing.
        # Need to implement this later

        # for point1 in points1:
        #     self.assertTrue(point1 in points2)
        #     points2.remove(point1)

    def assertGamesEqual(self, data1, data2):
        self.assertEqual(len(data1), len(data2))

        for i in range(len(data1)):
            self.assertGameEqual(data1[i], data2[i])

    def assertGameResponseEqual(self):
        self.assertResponse201()
        self.loadJSONSafely()

        self.assertGameEqual(self.responseData, self.check_against_data)
