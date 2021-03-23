from django.conf import settings
from django.db import models

from .managers import TeamManager


class Team(models.Model):
    PENDING = 'PD'
    DENIED = 'DE'
    ACCEPTED = 'AC'

    STATUS_OPTIONS = [
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (ACCEPTED, 'Accepted'),
    ]

    BRONZE = 'BR'
    SILVER = 'SR'
    GOLD = 'GD'
    PLATINUM = 'PL'
    DIAMOND = 'DI'

    LEAGUE_OPTIONS = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (PLATINUM, 'Platinum'),
        (DIAMOND, 'Diamond'),
    ]

    teamCaptain = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='teamCaptain')
    teammate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='teammate')

    status = models.CharField(max_length=2, choices=STATUS_OPTIONS,
                              default=PENDING)

    league = models.CharField(max_length=2, choices=LEAGUE_OPTIONS,
                              default=BRONZE)

    timeRequested = models.DateTimeField(auto_now_add=True)
    timeRespondedTo = models.DateTimeField(auto_now=True)

    objects = TeamManager()

    def __str__(self):
        return self.teamCaptain.username + " and " + self.teammate.username
