from rest_framework import authentication
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.my_auth.models import CustomUser
from apps.my_auth.serializers import BasicCustomUserSerializer

from .models import Friend
from .serializers import FriendCreateSerializer, FriendSerializer


class FriendListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    read_serializer = FriendSerializer
    write_serializer = FriendCreateSerializer

    def get_queryset(self):
        return Friend.objects.users_friends(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.write_serializer
        return self.read_serializer

    def create(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except Exception:
            pass
        request.data['team_captain'] = request.user.username

        try:
            request.data._mutable = False
        except Exception:
            pass
        return super().create(request, *args, **kwargs)


class AllUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = BasicCustomUserSerializer
    queryset = CustomUser.objects.all()
