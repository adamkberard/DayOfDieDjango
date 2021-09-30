from rest_framework import authentication
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated

from apps.games.models import Game
from apps.games.serializers import GameSerializer
from apps.players.models import Player

from .models import Team
from .serializers import TeamCreateSerializer, TeamSerializer


class TeamDetail(RetrieveUpdateAPIView):
    """
    View for getting a team

    * Requres token auth
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = TeamSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        if self.request.method == "PATCH":
            return Team.objects.get_player_teams(self.request.user)
        else:
            return Team.objects.all()


class TeamListCreate(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    read_serializer = TeamSerializer
    write_serializer = TeamCreateSerializer

    def get_queryset(self):
        return Team.objects.get_player_teams(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.write_serializer
        return self.read_serializer

    def get_serializer_context(self):
        return {'team_captain': self.request.user}


class GetPlayerTeams(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = TeamSerializer

    def get_queryset(self):
        urlUser = Player.objects.filter(uuid=self.kwargs['uuid'], is_staff=False)
        allTeams = Team.objects.get_player_teams(user=urlUser.first())
        return allTeams.filter(status=Team.STATUS_ACCEPTED)


class GetTeamGames(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer

    def get_queryset(self):
        print("HERE")
        urlTeam = Team.objects.filter(uuid=self.kwargs['uuid'])
        return Game.objects.get_team_games(urlTeam.first())
