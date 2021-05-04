from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Friend
from .serializers import FriendSerializer, FriendCreateSerializer


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
        if request.data.get('status') not in ['ac', 'dn']:
            request.data['status'] = 'ac'

        try:
            request.data._mutable = False
        except Exception:
            pass
        return super().create(request, *args, **kwargs)

class FriendRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = FriendSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Friend.objects.users_friends(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        # Make sure the requester isn't accepting their own request
        if self.checkIsRequesterAccepting(request.data, request.user):
            return Response(data={'errors': ["Can't accept friend request as sender."]},
                            status=403)
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Make sure the requester isn't accepting their own request
        if self.checkIsRequesterAccepting(request.data, request.user):
            return Response(data={'errors': ["Can't accept friend request as sender."]},
                            status=403)
        return self.update(request, *args, **kwargs)

    def checkIsRequesterAccepting(self, data, user):
        if 'status' in data:
            if data['status'] == 'ac':
                if self.get_object().team_captain == user:
                    return True
        return False
