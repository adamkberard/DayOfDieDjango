from django.contrib.auth.base_user import BaseUserManager


class TeamManager(BaseUserManager):
    """
    Custom team model manager to add my own filter thing
    """

    def users_teams(self, user):
        teamCaptains = super().get_queryset().filter(teammate=user)
        teammates = super().get_queryset().filter(teamCaptain=user)
        return teamCaptains | teammates
