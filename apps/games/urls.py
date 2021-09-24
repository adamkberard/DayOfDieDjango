from django.urls import path

from .views import (GameListCreateAPIView, GameRetrieveUpdateDestroyAPIView,
                    GetPlayerGames, GetTeamGames)

urlpatterns = [
    # /games/:username/
    path(
        route='<str:username1>/<str:username2>/',
        view=GetTeamGames.as_view(),
        name='game_rest_api_3'
    ),
    # /games/:username/
    path(
        route='<str:username>/',
        view=GetPlayerGames.as_view(),
        name='game_rest_api_2'
    ),
    # /games/
    path(
        route='',
        view=GameListCreateAPIView.as_view(),
        name='game_request_create'
    ),
    # /games/:uuid/
    path(
        route='<uuid:uuid>/',
        view=GameRetrieveUpdateDestroyAPIView.as_view(),
        name='game_rest_api_2'
    ),
]
