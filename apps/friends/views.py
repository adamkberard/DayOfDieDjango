from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Friend
from .serializers import FriendSerializer


class FriendDetailView(APIView):
    """
    View for single friend related requests

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request, friendId):
        """
        Return a single friend
        """
        try:
            usersFriendModels = Friend.objects.users_friends(user=request.user)
            friendModel = usersFriendModels.get(id=friendId)
        except Friend.DoesNotExist:
            returnData = {'error': 'Friend id not found: ' + str(friendId)}
            return Response(returnData)

        friendSerialized = FriendSerializer(friendModel)
        returnData = {'friend': friendSerialized.data}
        return Response(returnData)

    def delete(self, request, friendId):
        """
        Deletes a friend
        """
        try:
            usersFriendModels = Friend.objects.users_friends(user=request.user)
            friendModel = usersFriendModels.get(id=friendId)
        except Friend.DoesNotExist:
            returnData = {'error': 'Friend id not found: ' + str(friendId)}
            return Response(returnData)

        friendModel.delete()
        returnData = {'status': 'okay'}
        return Response(returnData)


class FriendView(APIView):
    """
    View for getting all lists, and posting

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            usersFriendModels = Friend.objects.users_friends(user=request.user)
        except Friend.DoesNotExist:
            returnData = {'error': 'Friend id not found: '}
            return Response(returnData)

        friendsSerialized = FriendSerializer(usersFriendModels, many=True)
        myOwnData = []
        for temp in friendsSerialized.data:
            myOwnData.append(temp)

        for friendData in myOwnData:
            for field in friendData:
                if field == 'friendOne':
                    if friendData['friendOne'] == request.user.username:
                        friendData['friend'] = friendData['friendTwo']
                        friendData.pop('friendOne', None)
                        friendData.pop('friendTwo', None)
                        break
                if field == 'friendTwo':
                    if friendData['friendTwo'] == request.user.username:
                        friendData['friend'] = friendData['friendOne']
                        friendData.pop('friendOne', None)
                        friendData.pop('friendTwo', None)
                        break

        returnData = {'friends': myOwnData}
        return Response(returnData)
