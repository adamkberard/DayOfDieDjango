from django.test import TestCase

from apps.my_auth.factories import CustomUserFactory

from ..factories import GameFactory, PointFactory
from ..models import Point
from ..serializers import GameSerializer, PointSerializer


class GameSerializerTests(TestCase):
    def test_regular_game_no_points(self):
        """Testing a regular game factory and serializer"""
        gameModel = GameFactory()
        serialized = GameSerializer(gameModel)
        sData = serialized.data

        # First I'll check the date times
        dateFormatString = "%Y-%m-%d %H:%M:%S"
        self.assertEqual(sData['timeStarted'],
                         gameModel.timeStarted.strftime(dateFormatString))
        self.assertEqual(sData['timeSaved'],
                         gameModel.timeSaved.strftime(dateFormatString))

        self.assertEqual(sData['statType'], gameModel.statType)

        # Then I check the playerId's
        fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
        for field in fields:
            self.assertEqual(sData[field], getattr(gameModel, field).username)


class PointSerializerTests(TestCase):
    def test_single_point(self):
        """Testing a single point factory and serializer"""
        user1 = CustomUserFactory()
        pointModel = PointFactory(scorer=user1, typeOfPoint=Point.SINGLE_POINT)
        serialized = PointSerializer(pointModel)
        sData = serialized.data

        self.assertEqual(sData['typeOfPoint'], pointModel.typeOfPoint)
        self.assertEqual(sData['scorer'], pointModel.scorer.username)
        self.assertEqual(sData['scoredOn'], None)

    def test_tink(self):
        """Testing a tink factory and serializer"""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        pointModel = PointFactory(scorer=user1, typeOfPoint=Point.TINK,
                                  inputScoredOn=user2)
        serialized = PointSerializer(pointModel)
        sData = serialized.data

        self.assertEqual(sData['typeOfPoint'], pointModel.typeOfPoint)
        self.assertEqual(sData['scorer'], pointModel.scorer.username)
        self.assertEqual(sData['scoredOn'], pointModel.scoredOn.username)

    def test_sink(self):
        """Testing a sink factory and serializer"""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        pointModel = PointFactory(scorer=user1, typeOfPoint=Point.SINK,
                                  inputScoredOn=user2)
        serialized = PointSerializer(pointModel)
        sData = serialized.data

        self.assertEqual(sData['typeOfPoint'], pointModel.typeOfPoint)
        self.assertEqual(sData['scorer'], pointModel.scorer.username)
        self.assertEqual(sData['scoredOn'], pointModel.scoredOn.username)

    def test_bounce_sink(self):
        """Testing a bounce sink factory and serializer"""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        pointModel = PointFactory(scorer=user1, typeOfPoint=Point.BOUNCE_SINK,
                                  inputScoredOn=user2)
        serialized = PointSerializer(pointModel)
        sData = serialized.data

        self.assertEqual(sData['typeOfPoint'], pointModel.typeOfPoint)
        self.assertEqual(sData['scorer'], pointModel.scorer.username)
        self.assertEqual(sData['scoredOn'], pointModel.scoredOn.username)

    def test_partner_sink(self):
        """Testing a partner sink factory and serializer"""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        pointModel = PointFactory(scorer=user1, typeOfPoint=Point.PARTNER_SINK,
                                  inputScoredOn=user2)
        serialized = PointSerializer(pointModel)
        sData = serialized.data

        self.assertEqual(sData['typeOfPoint'], pointModel.typeOfPoint)
        self.assertEqual(sData['scorer'], pointModel.scorer.username)
        self.assertEqual(sData['scoredOn'], pointModel.scoredOn.username)

    def test_self_sink(self):
        """Testing a self sink factory and serializer"""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        pointModel = PointFactory(scorer=user1, typeOfPoint=Point.SELF_SINK,
                                  inputScoredOn=user2)
        serialized = PointSerializer(pointModel)
        sData = serialized.data

        self.assertEqual(sData['typeOfPoint'], pointModel.typeOfPoint)
        self.assertEqual(sData['scorer'], pointModel.scorer.username)
        self.assertEqual(sData['scoredOn'], None)
