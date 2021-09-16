from django.contrib.auth.base_user import BaseUserManager

from apps.teams.models import Team


class GameManager(BaseUserManager):
    """
    Custom game model manager to add my own filter thing
    """

    def get_player_games(self, user):
        # First I get the teams the user in on
        teams = Team.objects.get_player_teams(user=user)
        teams_ones = super().get_queryset().filter(team_one__in=teams)
        teams_twos = super().get_queryset().filter(team_two__in=teams)
        return teams_ones | teams_twos

    def get_team_games(self, teams):
        teams_ones = super().get_queryset().filter(team_one=teams)
        teams_twos = super().get_queryset().filter(team_two=teams)
        return teams_ones | teams_twos

    def get_player_wins_losses(self, user):
        # First I get the teams the user in on
        teams = Team.objects.get_player_teams(user=user)
        wins = 0
        losses = 0

        for team in teams:
            for game in self.get_team_games(team):
                if game.didWin(team):
                    wins += 1
                else:
                    losses += 1

        return wins, losses
