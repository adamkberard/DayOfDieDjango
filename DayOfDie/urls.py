from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('laboratory/', admin.site.urls),
    path('game/', include('apps.games.urls')),
    path('friend/', include('apps.friends.urls')),
    path('team/', include('apps.teams.urls')),
    path('auth/', include('apps.my_auth.urls.auth_urls')),
]
