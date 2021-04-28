from django.conf import settings
import uuid as uuid_lib

from ..core.models import TimeStampedModel
from django.db import models

from .managers import FriendManager


class Friend(TimeStampedModel):
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

    STATUS_PENDING = 'pd'
    STATUS_ACCEPTED = 'ac'
    STATUS_DENIED = 'dn'
    STATUS_NOTHING = 'nt'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_DENIED, 'Denied'),
        (STATUS_NOTHING, 'Nothing'))

    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES
    )

    team_captain = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name="teamOne")
    teammate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="teamTwo")
    team_name = models.CharField(max_length=50, blank=True, null=True)

    wins = models.SmallIntegerField()
    losses = models.SmallIntegerField()

    league = models.CharField(
        max_length=2,
        choices=LEAGUE_CHOICES
    )

    objects = FriendManager()

    def __str__(self):
        return self.team_captain.email + " and " + self.teammate.email
