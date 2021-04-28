from django.db import IntegrityError
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from .models import CustomUser
from .serializers import CustomUserSerializer, MyAuthSerializer


class LoginView(CreateAPIView):
    """
    View for authenticating users
    """
    serializer_class = MyAuthSerializer


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
                estr = 'Could not create an account with those credentials.'
                returnData = {'errors': [estr]}
                return Response(returnData, status=401)

            # Gotta check if there's a token and create it if not
            # Then we send the token
            token, created = Token.objects.get_or_create(user=user)
            returnData = {'token': str(token),
                          'username': user.username}
            return Response(returnData, status=201)
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
        return Response(userSerialized.data, status=200)

    def post(self, request):
        """
        Updates an old litter
        """
        serialized = CustomUserSerializer(request.user, data=request.data,
                                          partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=200)
        else:
            return Response(serialized.errors, status=400)
