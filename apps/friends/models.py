from django.conf import settings
from django.db import models

from .managers import FriendManager


class Friend(models.Model):
    PENDING = 'PD'
    DENIED = 'DE'
    ACCEPTED = 'AC'

    STATUS_OPTIONS = [
        (PENDING, 'Pending'),
        (DENIED, 'Denied'),
        (ACCEPTED, 'Accepted'),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='requester')
    requested = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='requested')

    status = models.CharField(max_length=2, choices=STATUS_OPTIONS,
                              default=PENDING)

    timeRequested = models.DateTimeField(auto_now_add=True)
    timeRespondedTo = models.DateTimeField(auto_now=True)

    objects = FriendManager()

    def __str__(self):
        return self.playerOne.username + " and " + self.playerTwo.username
