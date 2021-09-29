from rest_framework import authentication
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated

from apps.players.models import Player
from apps.teams.models import Team

from .models import Game
from .serializers import GameSerializer, GameWriteSerializer


class GetPlayerGames(ListAPIView):
    """
    View for getting all a player's games

    * Requires player uuid
    * Requres token auth
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer

    def get_queryset(self):
        urlUser = Player.objects.filter(uuid=self.kwargs['uuid'], is_staff=False)
        return Game.objects.get_player_games(user=urlUser.first())


class GetTeamGames(ListAPIView):
    """
    View for getting all a team's games

    * Requires team uuid
    * Requres token auth
    """
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        urlUser1 = Player.objects.filter(username=self.kwargs['username1'], is_staff=False)
        urlUser2 = Player.objects.filter(username=self.kwargs['username2'], is_staff=False)
        urlTeam = Team.objects.get_team(urlUser1.first(), urlUser2.first())
        return Game.objects.get_team_games(urlTeam)


class GameDetail(RetrieveAPIView):
    """
    View for retrieving a single game

    * Requires a game uuid
    * Requres token auth
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer
    lookup_field = 'uuid'
    queryset = Game.objects.all()


class GameListCreate(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]

    read_serializer = GameSerializer
    write_serializer = GameWriteSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.write_serializer
        return self.read_serializer

    def get_queryset(self):
        return Game.objects.get_player_games(user=self.request.user)
