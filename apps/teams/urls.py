from django.urls import path

from .views import GetPlayerFriends, TeamListCreateAPIView

urlpatterns = [
    path(
        route='<str:username>/',
        view=GetPlayerFriends.as_view(),
        name='player_teams'
    ),
    path(
        route='',
        view=TeamListCreateAPIView.as_view(),
        name='team_generic'
    ),
]
