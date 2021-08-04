from rest_framework import authentication
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import Game
from .serializers import GameSerializer, GameWriteSerializer


class GameListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    #lookup_field = 'uuid'

    read_serializer = GameSerializer
    write_serializer = GameWriteSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.write_serializer
        return self.read_serializer

    def get_queryset(self):
        return Game.objects.users_games(user=self.request.user)

    def create(self, request, *args, **kwargs):        
        try:
            request.data._mutable = True
        except Exception:
            pass

        request.data['points'] = request.data.get('points', [])

        try:
            request.data._mutable = False
        except Exception:
            pass

        return super().create(request, *args, **kwargs)


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
