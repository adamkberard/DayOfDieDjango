from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.players.models import Player

from .serializers import LogInSerializer, RegisterSerializer


class LoginView(APIView):
    """
    View for authenticating users
    """
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Now we retrieve the user and send back their token.
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is None:
            return Response({'user': ['Not a valid user.']}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        content = {
            'token': str(token),
            'username': user.username
        }
        return Response(content, status=200)


class RegisterView(CreateAPIView):
    """
    View for registering users
    """
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = Player.objects.create_user(email=request.data['email'],
                                          password=request.data['password'])

        token, _ = Token.objects.get_or_create(user=user)
        content = {
            'token': str(token),
            'username': user.username
        }
        return Response(content, status=201)
