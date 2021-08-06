from django.contrib.auth.base_user import BaseUserManager

from apps.friends.models import Friend


class GameManager(BaseUserManager):
    """
    Custom game model manager to add my own filter thing
    """

    def users_games(self, user):
        # First I get the teams the user in on
        teams = Friend.objects.users_friends(user=user)
        team_ones = super().get_queryset().filter(team_one__in=teams)
        team_twos = super().get_queryset().filter(team_two__in=teams)
        return team_ones | team_twos

    def friends_games(self, friends):
        team_ones = super().get_queryset().filter(team_one=friends)
        team_twos = super().get_queryset().filter(team_two=friends)
        return team_ones | team_twos
