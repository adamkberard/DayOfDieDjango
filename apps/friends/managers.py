import random

from django.contrib.auth.base_user import BaseUserManager


class FriendManager(BaseUserManager):
    """
    Custom friend model manager to add my own filter thing
    """
    
    def getFriends(self, user):
        teammates = super().get_queryset().filter(teamCaptain=user).teammate
        captains = super().get_queryset().filter(teammate=user).teamCaptain
        return teammates | captains
