from django.contrib.auth.base_user import BaseUserManager


class GameManager(BaseUserManager):
    """
    Custom game model manager to add my own filter thing
    """

    def users_games(self, user):
        p1 = super().get_queryset().filter(playerOne=user)
        p2 = super().get_queryset().filter(playerTwo=user)
        p3 = super().get_queryset().filter(playerThree=user)
        p4 = super().get_queryset().filter(playerFour=user)
        return p1 | p2 | p3 | p4
