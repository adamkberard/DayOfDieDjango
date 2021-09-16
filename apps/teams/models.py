import uuid as uuid_lib

from django.conf import settings
from django.db import models

from ..core.models import TimeStampedModel
from .managers import TeamManager


class Team(TimeStampedModel):
    LEAGUE_UNRANKED = 'ur'
    LEAGUE_BRONZE = 'br'
    LEAGUE_SILVER = 'sv'
    LEAGUE_GOLD = 'gd'
    LEAGUE_DIAMOND = 'dm'

    LEAGUE_CHOICES = (
        (LEAGUE_UNRANKED, 'Unranked'),
        (LEAGUE_BRONZE, 'Bronze'),
        (LEAGUE_SILVER, 'Silver'),
        (LEAGUE_GOLD, 'Gold'),
        (LEAGUE_DIAMOND, 'Diamond'))

    STATUS_BLOCKED = 'bl'
    STATUS_PENDING = 'pd'
    STATUS_ACCEPTED = 'ac'
    STATUS_NOTHING = 'nt'

    STATUS_CHOICES = (
        (STATUS_BLOCKED, 'Blocked'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_NOTHING, 'Nothing'))

    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        primary_key=True
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    team_captain = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name="team_captain")
    teammate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="teammate")

    objects = TeamManager()

    def __str__(self):
        return self.team_captain.username + " and " + self.teammate.username

    def is_captain(self, user):
        return self.team_captain == user

    def __eq__(self, other):
        return (self.team_captain == other.team_captain and self.teammate == other.teammate or
                self.team_captain == other.teammate and self.teammate == other.team_captain)
