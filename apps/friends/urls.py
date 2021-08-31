from django.urls import path

from .views import FriendListCreateAPIView

urlpatterns = [
    path(
        route='',
        view=FriendListCreateAPIView.as_view(),
        name='friend_generic'
    ),
]
