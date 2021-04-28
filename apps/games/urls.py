from django.urls import path
from .views import GameListCreateAPIView, GameRetrieveUpdateDestroyAPIView
from .views import PointListCreateAPIView, PointRetrieveUpdateDestroyAPIView, PointListAPIView

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
    # /games/:uuid/points/
    path(
        route='<uuid:uuid>/points/',
        view=PointListAPIView.as_view(),
        name='point_rest_api_1'
    ),
    # /games/points/
    path(
        route='points/',
        view=PointListCreateAPIView.as_view(),
        name='point_rest_api_2'
    ),
    # /games/points/:uuid/
    path(
        route='points/<uuid:uuid>/',
        view=PointRetrieveUpdateDestroyAPIView.as_view(),
        name='point_rest_api_3'
    )
]
