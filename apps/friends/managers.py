from django.contrib.auth.base_user import BaseUserManager


class FriendManager(BaseUserManager):
    """
    Custom friend model manager to add my own filter thing
    """

    def users_friends(self, user):
        friendOnes = super().get_queryset().filter(friendTwo=user)
        friendTwos = super().get_queryset().filter(friendOne=user)
        return friendOnes | friendTwos
