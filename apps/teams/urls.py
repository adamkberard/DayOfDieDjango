from django.urls import path

from .views import GetTeamGames, TeamDetail, TeamListCreate

urlpatterns = [
    path(route='<uuid:uuid>/', view=TeamDetail.as_view(), name='TeamDetail'),
    path(route='<uuid:uuid>/games/', view=GetTeamGames.as_view(), name='GetTeamGames'),
    path(route='', view=TeamListCreate.as_view(), name='TeamListCreate')
]
