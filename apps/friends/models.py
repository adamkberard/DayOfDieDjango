from django.conf import settings
from django.db import models

from .managers import FriendManager


class Friend(models.Model):
    teamCaptain = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name="teamCaptain")
    teammate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="teammate")

    objects = FriendManager()

    def __str__(self):
        return self.teamCaptain.username + " and " + self.teammate.username
