from django.urls import path

from apps.games.views import GetPlayerGames
from apps.players.views import PlayerDetail, PlayerList
from apps.teams.views import GetPlayerTeams

urlpatterns = [
    path('<uuid:uuid>/games/', GetPlayerGames.as_view(), name='GetPlayerGames'),
    path('<uuid:uuid>/teams/', GetPlayerTeams.as_view(), name='GetPlayerTeams'),
    path('<uuid:uuid>/', PlayerDetail.as_view(), name='PlayerDetail'),
    path('', PlayerList.as_view(), name='PlayerList'),
]
