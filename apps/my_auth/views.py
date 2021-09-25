from django.contrib.auth import authenticate
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (CustomUserReadSerializer, CustomUserWriteSerializer,
                          LogInSerializer, RegisterSerializer)


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
        user = CustomUser.objects.create_user(email=request.data['email'],
                                              password=request.data['password'])

        token, _ = Token.objects.get_or_create(user=user)
        content = {
            'token': str(token),
            'username': user.username
        }
        return Response(content, status=201)


class UserView(ListAPIView):
    """
    View for getting all users

    * Requres token auth
    """
    serializer_class = CustomUserReadSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    queryset = CustomUser.objects.filter(is_staff=False)
    lookup_field = 'username'


class DetailUserView(RetrieveUpdateAPIView):
    """
    View for getting and setting usernames

    * Requires username
    * Requres token auth
    """
    read_serializer = CustomUserReadSerializer
    write_serializer = CustomUserWriteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]
    lookup_field = 'username'
    queryset = CustomUser.objects.filter(is_staff=False)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return self.write_serializer
        return self.read_serializer

    def get_serializer_context(self):
        return {'requester': self.request.user}
