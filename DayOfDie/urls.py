from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('laboratory/', admin.site.urls),
    path('games/', include('apps.games.urls')),
    path('friends/', include('apps.friends.urls')),
    path('auth/', include('apps.my_auth.urls.auth_urls')),
    path('users/', include('apps.my_auth.urls.user_urls')),
]
