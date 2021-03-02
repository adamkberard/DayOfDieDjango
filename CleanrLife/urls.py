from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.my_auth.urls.auth_urls')),
    path('litter/', include('apps.litter.urls')),
    path('user/', include('apps.my_auth.urls.user_urls')),
]
