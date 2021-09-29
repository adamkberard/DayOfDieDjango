from rest_framework import authentication
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from .models import Player
from .serializers import PlayerReadSerializer, PlayerWriteSerializer


class PlayerList(ListAPIView):
    """
    View for getting all players

    * Requres token auth
    """
    serializer_class = PlayerReadSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    queryset = Player.objects.filter(is_staff=False)
    lookup_field = 'username'


class PlayerDetail(RetrieveUpdateAPIView):
    """
    View for getting detailed player view

    * Requires username
    * Requres token auth
    """
    read_serializer = PlayerReadSerializer
    write_serializer = PlayerWriteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]
    lookup_field = 'uuid'
    queryset = Player.objects.filter(is_staff=False)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return self.write_serializer
        return self.read_serializer

    def get_serializer_context(self):
        return {'requester': self.request.user}
