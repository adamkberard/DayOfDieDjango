from rest_framework import authentication
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from apps.my_auth.models import CustomUser
from apps.teams.models import Team

from .models import Game
from .serializers import GameSerializer, GameWriteSerializer


class GameListCreateAPIView(ListCreateAPIView):
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


class GameRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Getting, updating, or deleting an existing game
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Game.objects.get_player_games(user=self.request.user)


class GameRetrieveTeamsAPIView(RetrieveUpdateDestroyAPIView):
    """
    Getting, updating, or deleting an existing game
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Game.objects.get_player_games(user=self.request.user)


class GetPlayerGames(ListAPIView):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        urlUser = CustomUser.objects.filter(username=self.kwargs['username'])
        return Game.objects.get_player_games(user=urlUser.first())


class GetTeamGames(ListAPIView):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        urlUser1 = CustomUser.objects.filter(username=self.kwargs['username1'])
        urlUser2 = CustomUser.objects.filter(username=self.kwargs['username2'])
        urlTeam = Team.objects.get_team(urlUser1.first(), urlUser2.first())
        return Game.objects.get_team_games(urlTeam)
