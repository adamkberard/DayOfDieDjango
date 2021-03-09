from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer, MyAuthSerializer


class LoginView(APIView):
    """
    View for authenticating users

    * Requires email, password
    """
    serializer_class = MyAuthSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request):
        """
        Returns a token if the login is successfull
        """

        data = JSONParser().parse(request)
        serializer = MyAuthSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(username=email, password=password)

            if user is None:
                # Just gotta say shits wrong
                returnData = {'error': 'Email or password wrong.'}
                return Response(returnData, status=401)
            else:
                # Gotta check if there's a token and create it if not
                # Then we send the token
                token, created = Token.objects.get_or_create(user=user)
                returnData = {'token': str(token),
                              'username': user.username}
                return Response(returnData)
        return Response(serializer.errors, status=400)


class RegisterView(APIView):
    """
    View for registering users

    * Requires email, password
    """
    serializer_class = MyAuthSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = MyAuthSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']

            try:
                user = CustomUser.objects.create_user(email, password=password)
            except IntegrityError:
                eString = 'Could not create an account with those credentials.'
                returnData = {'error': eString}
                return Response(returnData, status=401)

            if user is None:
                # Just gotta say shits wrong
                returnData = {'error': 'Username or password wrong.'}
                return Response(returnData)
            else:
                # Gotta check if there's a token and create it if not
                # Then we send the token
                token, created = Token.objects.get_or_create(user=user)
                returnData = {'token': str(token),
                              'username': user.username}
                return Response(returnData)
        return Response(serializer.errors, status=400)


class UserView(APIView):
    """
    View for getting and setting usernames

    * Requires username
    * Requres token auth
    """
    serializer_class = CustomUserSerializer

    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """
        Returns the user data, what that is is TBD
        """
        userSerialized = CustomUserSerializer(request.user)
        return Response(userSerialized.data)

    def post(self, request):
        """
        Updates an old litter
        """
        serialized = CustomUserSerializer(request.user, data=request.data,
                                          partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors, status=400)
