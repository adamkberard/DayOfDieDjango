from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Game, Point
from .serializers import GameSerializer, PointSerializer


class GameListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = GameSerializer
    lookup_field = 'uuid'

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


class PointListCreateAPIView(ListAPIView):
    """
    Getting all of a users points and also creating
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PointSerializer

    def get_queryset(self):
        return Point.objects.filter(scorer=self.request.user)

    # def post(self, request, *args, **kwargs):
    #     """
    #     #checks if post request data is an array initializes serializer with many=True
    #     else executes default CreateModelMixin.create function
    #     """
    #     is_many = isinstance(request.data, list)
    #     if not is_many:
    #         return super(BookViewSet, self).create(request, *args, **kwargs)
    #     else:
    #         serializer = self.get_serializer(data=request.data, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=201)


class PointRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Getting, updating, or deleting an individual point
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PointSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Point.objects.filter(scorer=self.request.user)


class PointListAPIView(ListAPIView):
    """
    For getting all the points from a game
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PointSerializer

    def get_queryset(self):
        try:
            print(self.kwargs)
            game = Game.objects.get(uuid=self.kwargs['uuid'])
        except Game.DoesNotExist:
            return Response(data={'detail': "Game not found."}, status=404)
        return Point.objects.filter(game=game)
