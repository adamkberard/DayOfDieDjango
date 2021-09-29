from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('laboratory/', admin.site.urls),
    path('auth/', include('apps.my_auth.urls')),
    path('player/', include('apps.players.urls')),
    path('team/', include('apps.teams.urls')),
    path('game/', include('apps.games.urls')),
]
