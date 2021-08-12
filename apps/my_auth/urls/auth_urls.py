from django.urls import path

from ..views import LoginView, RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='my_login'),
    path('register/', RegisterView.as_view(), name='my_register')
]
