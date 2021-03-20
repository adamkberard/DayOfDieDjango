from django.urls import path, register_converter

from tools.ids_encoder import converters

from .views import GameDetailView, GameView

register_converter(converters.HashidsConverter, 'hashids')

urlpatterns = [
    path('', GameView.as_view(), name='game_list'),
    path('<hashids:gameId>/', GameDetailView.as_view(), name='game_detail'),
    path('<hashids:gameId>/', GameDetailView.as_view(),
         name='game_detail'),
]
