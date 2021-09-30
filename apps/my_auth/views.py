from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.players.models import Player

from .serializers import LogInSerializer, RegisterSerializer


class LoginView(CreateAPIView):
    """
    View for authenticating users
    """
    renderer_classes = [JSONRenderer]
    serializer_class = LogInSerializer


class RegisterView(CreateAPIView):
    """
    View for registering users
    """
    renderer_classes = [JSONRenderer]
    serializer_class = RegisterSerializer
