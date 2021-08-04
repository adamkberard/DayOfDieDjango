from django.urls import path

from .views import GameListCreateAPIView, GameRetrieveUpdateDestroyAPIView

urlpatterns = [
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
