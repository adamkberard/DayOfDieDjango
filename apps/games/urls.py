from django.urls import path, register_converter

from tools.ids_encoder import converters

from .views import GameDetailView, GameView, gameStats

register_converter(converters.HashidsConverter, 'hashids')

urlpatterns = [
    path('', GameView.as_view(), name='game_list'),
    path('<hashids:pk>/', GameDetailView.as_view(), name='game_detail'),
]
