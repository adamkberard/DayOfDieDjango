from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Friend
from .serializers import FriendSerializer


class FriendListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = FriendSerializer

    def get_queryset(self):
        return Friend.objects.users_friends(user=self.request.user)


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
