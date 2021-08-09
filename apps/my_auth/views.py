from apps.my_auth.tests.factories import CustomUserFactory
from django.utils.translation import deactivate_all
from rest_framework import authentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser

from .serializers import (CustomUserSerializer, MyLogInSerializer,
                          MyRegisterSerializer, CustomUserPageSerializer)


class LoginView(CreateAPIView):
    """
    View for authenticating users
    """
    serializer_class = MyLogInSerializer


class RegisterView(CreateAPIView):
    """
    View for registering users
    """
    serializer_class = MyRegisterSerializer


class UserView(ListAPIView):
    """
    View for getting and setting usernames

    * Requires username
    * Requres token auth
    """
    serializer_class = CustomUserPageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    queryset = CustomUser.objects.all()
    lookup_field = 'username'


class DetailUserView(RetrieveUpdateAPIView):
    """
    View for getting and setting usernames

    * Requires username
    * Requres token auth
    """
    serializer_class = CustomUserPageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    queryset = CustomUser.objects.all()
    lookup_field = 'username'