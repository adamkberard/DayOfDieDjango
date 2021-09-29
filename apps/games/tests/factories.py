import datetime

import factory
import factory.fuzzy
import pytz

from apps.players.tests.factories import PlayerFactory
from apps.teams.tests.factories import TeamFactory

from ..models import Game, Point


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point

    class Params:
        inputScoredOn = factory.SubFactory(PlayerFactory)

    scorer = factory.SubFactory(PlayerFactory)
    typeOfPoint = factory.fuzzy.FuzzyChoice(item[0] for item in
                                            Point.TYPE_CHOICES)
    scoredOn = factory.LazyAttribute(lambda x: x.inputScoredOn
                                     if x.typeOfPoint
                                     in ['TK', 'SK', 'BS', 'PS'] else None)


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    time_started = factory.fuzzy.FuzzyDateTime(datetime.datetime(2021, 3, 12, tzinfo=pytz.utc))
    time_ended = factory.LazyAttribute(lambda o: o.time_started + datetime.timedelta(minutes=25))
    home_team = factory.SubFactory(TeamFactory)
    away_team = factory.SubFactory(TeamFactory)

    home_team_score = 11
    away_team_score = 9

    confirmed = False
