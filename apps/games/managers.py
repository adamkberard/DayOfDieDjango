from apps.friends.serializers import FriendSerializer
from django.contrib.auth.base_user import BaseUserManager

from apps.friends.models import Friend


class GameManager(BaseUserManager):
    """
    Custom game model manager to add my own filter thing
    """

    def users_games(self, user):
        # First I get the teams the user in on
        friends = Friend.objects.users_friends(user=user)
        friends_ones = super().get_queryset().filter(team_one__in=friends)
        friends_twos = super().get_queryset().filter(team_two__in=friends)
        return friends_ones | friends_twos

    def friends_games(self, friends):
        friends_ones = super().get_queryset().filter(team_one=friends)
        friends_twos = super().get_queryset().filter(team_two=friends)
        return friends_ones | friends_twos
    
    def users_wins_losses(self, user):
        # First I get the teams the user in on
        friends = Friend.objects.users_friends(user=user)
        wins = 0
        losses = 0

        for friend in friends:
            for game in self.friends_games(friend):
                if game.didWin(friend):
                    wins += 1
                else:
                    losses += 1

        return wins, losses
