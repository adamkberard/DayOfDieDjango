from django.contrib.auth.base_user import BaseUserManager


class FriendManager(BaseUserManager):
    """
    Custom friend model manager to add my own filter thing
    """

    def users_friends(self, user):
        requesters = super().get_queryset().filter(requested=user)
        requesteds = super().get_queryset().filter(requester=user)
        return requesters | requesteds
