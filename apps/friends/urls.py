from django.urls import path
from .views import FriendListCreateAPIView, FriendRetrieveUpdateAPIView

urlpatterns = [
    # /flavors/api/
    path(
        route='',
        view=FriendListCreateAPIView.as_view(),
        name='friend_rest_api_1'
    ),
    # /flavors/api/:uuid/
    path(
        route='<uuid:uuid>/',
        view=FriendRetrieveUpdateAPIView.as_view(),
        name='friend_rest_api_2'
    )
]
