import datetime

import factory
import factory.fuzzy
import pytz

from apps.my_auth.factories import CustomUserFactory

from .models import Game, Point


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point

    class Params:
        inputScoredOn = factory.SubFactory(CustomUserFactory)

    scorer = factory.SubFactory(CustomUserFactory)
    typeOfPoint = factory.fuzzy.FuzzyChoice(item[0] for item in
                                            Point.POINT_TYPE_CHOICES)
    scoredOn = factory.LazyAttribute(lambda x: x.inputScoredOn
                                     if x.typeOfPoint
                                     in ['TK', 'SK', 'BS', 'PS'] else None)


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    timeStarted = factory.fuzzy.FuzzyDateTime(datetime.datetime(2021, 3, 12,
                                              tzinfo=pytz.utc))
    timeSaved = factory.LazyAttribute(lambda o: o.timeStarted +
                                      datetime.timedelta(minutes=25))
    playerOne = factory.SubFactory(CustomUserFactory)
    playerTwo = factory.SubFactory(CustomUserFactory)
    playerThree = factory.SubFactory(CustomUserFactory)
    playerFour = factory.SubFactory(CustomUserFactory)
