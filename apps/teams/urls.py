from django.urls import path, register_converter

from tools.ids_encoder import converters

from .views import TeamDetailView, TeamView

register_converter(converters.HashidsConverter, 'hashids')

urlpatterns = [
    path('', TeamView.as_view(), name='team_list'),
    path('<hashids:teamId>/', TeamDetailView.as_view(),
         name='team_detail'),
]
