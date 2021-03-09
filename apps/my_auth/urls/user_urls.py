from django.urls import path

from ..views import UserView

# from django.urls import register_converter
# from tools.ids_encoder import converters

# register_converter(converters.HashidsConverter, 'hashids')

urlpatterns = [
    path('users/', UserView.as_view(), name='my_username'),
    # path('users/<hashids:user_id>/', test_user_id, name='test_user_id'),
]
