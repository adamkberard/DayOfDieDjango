from django.urls import path

from .views import FriendListCreateAPIView

urlpatterns = [
    # /flavors/api/
    path(
        route='',
        view=FriendListCreateAPIView.as_view(),
        name='friend_request_create'
    ),
]
