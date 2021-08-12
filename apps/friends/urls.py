from django.urls import path

from .views import AllUsersAPIView, FriendListCreateAPIView

urlpatterns = [
    path(
        route='all_users',
        view=AllUsersAPIView.as_view(),
        name='get_all_users'
    ),
    path(
        route='',
        view=FriendListCreateAPIView.as_view(),
        name='friend_request_create'
    ),
]
