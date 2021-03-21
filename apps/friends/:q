from django.urls import path, register_converter

from tools.ids_encoder import converters

from .views import FriendDetailView, FriendView

register_converter(converters.HashidsConverter, 'hashids')

urlpatterns = [
    path('', FriendView.as_view(), name='friend_list'),
    path('<hashids:friendId>/', FriendDetailView.as_view(),
         name='friend_detail'),
]
