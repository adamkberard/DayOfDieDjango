from django.urls import path

from .views import TeamListCreateAPIView

urlpatterns = [
    path(
        route='',
        view=TeamListCreateAPIView.as_view(),
        name='team_generic'
    ),
]
