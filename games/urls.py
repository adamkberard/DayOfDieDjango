from .views import gameCRUD, gameCRUDDetail
from django.urls import path

urlpatterns = [
    path('', gameCRUD, name='game-crud'),
    path('<int:gameId>/', gameCRUDDetail, name='game-crud-detail'),
]
