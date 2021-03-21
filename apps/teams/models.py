from django.conf import settings
from django.db import models

# from .managers import FriendManager


class Team(models.Model):
    BRONZE = 'BR'
    SILVER = 'SR'
    GOLD = 'GD'
    DIAMOND = 'DM'

    LEAGUE_OPTIONS = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (DIAMOND, 'Diamond'),
    ]

    PENDING = 'PD'
    DENIED = 'DE'
    ACCEPTED = 'AC'

    STATUS_OPTIONS = [
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (ACCEPTED, 'Accepted'),
    ]

    league = models.CharField(max_length=2, choices=LEAGUE_OPTIONS,
                              default=BRONZE)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS,
                              default=PENDING)

    teamCaptain = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='teamCaptain')
    teammate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='teammate')

    timeRequested = models.DateTimeField(auto_now_add=True)
    timeRespondedTo = models.DateTimeField(auto_now=True)

#    objects = FriendManager()

    def __str__(self):
        return self.teamCaptain.username + " and " + self.teammate.username
