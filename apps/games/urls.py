from django.urls import path

from .views import GameDetail, GameListCreate

urlpatterns = [
    # /games/
    path(route='<uuid:uuid>/', view=GameDetail.as_view(), name='GameDetail'),
    path(route='', view=GameListCreate.as_view(), name='GameListCreate'),
]
