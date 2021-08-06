from django.contrib.auth.base_user import BaseUserManager


class FriendManager(BaseUserManager):
    """
    Custom friend model manager to add my own filter thing
    """

    def users_friends(self, user):
        team_captains = super().get_queryset().filter(teammate=user)
        teammates = super().get_queryset().filter(team_captain=user)
        return team_captains | teammates

    def get_friendship(self, user1, user2):
        possibility = super().get_queryset().filter(team_captain=user1, teammate=user2).first()
        if possibility is not None:
            return possibility

        possibility = super().get_queryset().filter(team_captain=user2, teammate=user1).first()
        if possibility is not None:
            return possibility

        return None

    def friendship_exists(self, user1, user2):
        possibility = super().get_queryset().filter(team_captain=user1, teammate=user2).first()
        if possibility is not None:
            return True

        possibility = super().get_queryset().filter(team_captain=user2, teammate=user1).first()
        if possibility is not None:
            return True

        return False

    def get_or_create_friend(self, user1, user2):
        if(self.friendship_exists(user1, user2)):
            return False, self.get_friendship(user1, user2)

        friend = super().create(status='nt',
                                team_captain=user1,
                                teammate=user2
                                )

        # Returning whether or not the friendship was created, and the friendship
        return True, friend
