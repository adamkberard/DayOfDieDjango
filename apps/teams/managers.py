from django.contrib.auth.base_user import BaseUserManager


class TeamManager(BaseUserManager):
    """
    Custom team model manager to add my own filter thing
    """

    def get_player_teams(self, user):
        team_captains = super().get_queryset().filter(teammate=user)
        teammates = super().get_queryset().filter(team_captain=user)
        return team_captains | teammates

    def get_team(self, user1, user2):
        possibility = super().get_queryset().filter(team_captain=user1, teammate=user2).first()
        if possibility is not None:
            return possibility

        possibility = super().get_queryset().filter(team_captain=user2, teammate=user1).first()
        if possibility is not None:
            return possibility

        return None

    def team_exists(self, user1, user2):
        possibility = super().get_queryset().filter(team_captain=user1, teammate=user2).first()
        if possibility is not None:
            return True

        possibility = super().get_queryset().filter(team_captain=user2, teammate=user1).first()
        if possibility is not None:
            return True

        return False

    def get_or_create_team(self, user1, user2):
        if(self.team_exists(user1, user2)):
            return False, self.get_team(user1, user2)

        team = super().create(status='nt',
                              team_captain=user1,
                              teammate=user2)

        # Returning whether or not the teamship was created, and the teamship
        return True, team
