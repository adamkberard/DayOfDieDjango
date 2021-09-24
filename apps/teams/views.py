from rest_framework import authentication
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.my_auth.models import CustomUser

from .models import Team
from .serializers import TeamCreateSerializer, TeamSerializer


class TeamListCreateAPIView(ListCreateAPIView):
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


class GetPlayerFriends(ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        urlUser = CustomUser.objects.filter(username=self.kwargs['username'])
        allTeams = Team.objects.get_player_teams(user=urlUser.first())
        return allTeams.filter(status=Team.STATUS_ACCEPTED)
