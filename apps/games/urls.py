from .views import gameCRUD, gameCRUDDetail, gameStats
from django.urls import path

urlpatterns = [
    path('', gameCRUD, name='game-crud'),
    path('<int:gameId>/', gameCRUDDetail, name='game-crud-detail'),
    path('stats/', gameStats, name='game-stats'),
]
