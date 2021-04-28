from django.contrib.auth.base_user import BaseUserManager


class FriendManager(BaseUserManager):
    """
    Custom friend model manager to add my own filter thing
    """

    def users_friends(self, user):
        team_captains = super().get_queryset().filter(teammate=user)
        teammates = super().get_queryset().filter(team_captain=user)
        return team_captains | teammates

    def get_or_create_friend(self, user1, user2):
        possibility = super().get_queryset().filter(team_captain=user1, teammate=user2).first()
        if possibility is not None:
            return possibility

        possibility = super().get_queryset().filter(team_captain=user2, teammate=user1).first()
        if possibility is not None:
            return possibility

        friend = super().create(status=Friend.STATUS_NOTHING,
                                team_captain=user1,
                                teammate=user2,
                                wins=0,
                                losses=0,
                                league=Friend.LEAGUE_UNRANKED)

        return friend
