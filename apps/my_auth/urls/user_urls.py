from django.urls import path

from ..views import DetailUserView, UserView

urlpatterns = [
    path('<str:username>/', DetailUserView.as_view(), name='detail_user_view'),
    path('', UserView.as_view(), name='user_view'),
]
