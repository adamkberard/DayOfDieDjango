from rest_framework import authentication
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

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
        return Game.objects.users_games(user=self.request.user)


class GameRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Getting, updating, or deleting an existing game
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Game.objects.users_games(user=self.request.user)


class GameRetrieveTeamsAPIView(RetrieveUpdateDestroyAPIView):
    """
    Getting, updating, or deleting an existing game
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Game.objects.users_games(user=self.request.user)
