from django.urls import path

from .views import GameListCreateAPIView, GameRetrieveUpdateDestroyAPIView

urlpatterns = [
    # /games/
    path(
        route='',
        view=GameListCreateAPIView.as_view(),
        name='game_rest_api_1'
    ),
    # /games/:uuid/
    path(
        route='<uuid:uuid>/',
        view=GameRetrieveUpdateDestroyAPIView.as_view(),
        name='game_rest_api_2'
    ),
]
