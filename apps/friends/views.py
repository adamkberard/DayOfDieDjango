from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.my_auth.models import CustomUser

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

    def put(self, request, friendId):
        """
        Edits a single friend
        """
        try:
            usersFriendModels = Friend.objects.users_friends(user=request.user)
            friendModel = usersFriendModels.get(id=friendId)
        except Friend.DoesNotExist:
            returnData = {'error': 'Friend id not found: ' + str(friendId)}
            return Response(returnData)

        if 'status' in request.data:
            if request.data['status'] == 'accept':
                # They can only accept it if they are the requested
                if request.user == friendModel.requester:
                    errStr = 'Cannot accept a friend request as the requester.'
                    return Response({'error': errStr})
                else:
                    friendModel.status = friendModel.ACCEPTED
                    friendModel.save()
            elif request.data['status'] == 'deny':
                if request.user == friendModel.requester:
                    errStr = 'Cannot deny a friend request as the requester.'
                    return Response({'error': errStr})
                else:
                    friendModel.status = friendModel.DENIED
                    friendModel.save()

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
                if field == 'requester':
                    if friendData['requester'] == request.user.username:
                        friendData['friend'] = friendData['requested']
                        friendData.pop('requester', None)
                        friendData.pop('requested', None)
                        break
                if field == 'requested':
                    if friendData['requested'] == request.user.username:
                        friendData['friend'] = friendData['requester']
                        friendData.pop('requester', None)
                        friendData.pop('requested', None)
                        break

        returnData = {'friends': myOwnData}
        return Response(returnData)

    def post(self, request):
        """Posting a new friend. Pretty simple stuff"""
        if 'friend' not in request.data:
            data = {'friend': ['This field is required.']}
            return Response(data=data, status=400)

        # Making sure the incoming friend exists
        usrname = request.data['friend']
        try:
            friendModel = CustomUser.objects.get(username=usrname)
        except CustomUser.DoesNotExist:
            errStr = 'Cannot find a user with username: {}'.format(usrname)
            returnData = {'error': errStr}
            return Response(returnData)

        # Creating friendship, default is pending so that works out
        friendshipModel = Friend(requester=request.user, requested=friendModel)
        friendshipModel.save()
        friendshipSerialized = FriendSerializer(friendshipModel)

        returnData = {'friend': friendshipSerialized.data}
        return Response(returnData)
