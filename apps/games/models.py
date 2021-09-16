import uuid as uuid_lib

from django.conf import settings
from django.db import models

from ..core.models import TimeStampedModel
from ..teams.models import Team
from .managers import GameManager


class Game(TimeStampedModel):
    TYPE_PICKUP = 'pu'
    TYPE_MARATHON = 'ma'
    TYPE_TOURNAMENT = 'tm'

    TYPE_CHOICES = (
        (TYPE_PICKUP, 'Pickup Game'),
        (TYPE_MARATHON, 'Marathon Game'),
        (TYPE_TOURNAMENT, 'Tournament Game')
    )

    time_started = models.DateTimeField()
    time_ended = models.DateTimeField()

    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        primary_key=True
    )

    team_one = models.ForeignKey(Team,
                                 on_delete=models.CASCADE,
                                 related_name="team_one")
    team_two = models.ForeignKey(Team,
                                 on_delete=models.CASCADE,
                                 related_name="team_two")

    team_one_score = models.SmallIntegerField()
    team_two_score = models.SmallIntegerField()

    confirmed = models.BooleanField()

    objects = GameManager()

    # TODO
    def didWin(self, team):
        if self.team_one == team:
            return self.team_one_score > self.team_two_score
        if self.team_two == team:
            return self.team_two_score > self.team_one_score
        return False

    def __str__(self):
        return str(self.time_started)


class Point(TimeStampedModel):
    TYPE_SINGLE = 'sg'
    TYPE_TINK = 'tk'
    TYPE_SINK = 'sk'
    TYPE_BOUNCE_SINK = 'bs'
    TYPE_PARTNER_SINK = 'ps'
    TYPE_SELF_SINK = 'ss'
    TYPE_FIFA = 'ff'
    TYPE_FIELD_GOAL = 'fg'
    TYPE_FIVE = 'fv'
    TYPE_UNTRACKED = 'ut'

    TYPE_CHOICES = (
        (TYPE_SINGLE, 'Single Point'),
        (TYPE_TINK, 'Tink'),
        (TYPE_SINK, 'Sink'),
        (TYPE_BOUNCE_SINK, 'Bounce Sink'),
        (TYPE_PARTNER_SINK, 'Partner Sink'),
        (TYPE_SELF_SINK, 'Self Sink'),
        (TYPE_FIFA, 'Fifa'),
        (TYPE_FIELD_GOAL, 'Field Goal'),
        (TYPE_FIVE, 'Five'),
        (TYPE_UNTRACKED, 'Untracked'),
    )

    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        primary_key=True
    )

    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_SINGLE)

    scorer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="scorer")

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="game")

    objects = GameManager()

    def __str__(self):
        return str('{} scored a {}'.format(self.scorer.username, self.type))
