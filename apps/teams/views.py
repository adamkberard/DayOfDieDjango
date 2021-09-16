from rest_framework import authentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

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
