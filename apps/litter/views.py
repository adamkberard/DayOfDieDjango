from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Litter
from .serializers import LitterSerializer


class LitterViewDetail(APIView):
    """
    View for single litter related requests

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request, litterId):
        """
        Return a single piece of litter
        """
        try:
            litterModel = Litter.objects.get(user=request.user, id=litterId)
        except Litter.DoesNotExist:
            errors = {'litterId': 'Litter id not found: ' + str(litterId)}
            returnData = {'errors': errors}
            return Response(returnData)

        litterSerialized = LitterSerializer(litterModel)
        return Response(litterSerialized.data)

    def put(self, request, litterId):
        """
        Updates an old litter
        """
        try:
            litterModel = Litter.objects.get(user=request.user, id=litterId)
        except Litter.DoesNotExist:
            errors = {'litterId': 'Litter id not found: ' + str(litterId)}
            returnData = {'errors': errors}
            return Response(returnData)

        serialized = LitterSerializer(litterModel, data=request.data)

        if serialized.is_valid():
            litterModel = serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors, status=400)

    def delete(self, request, litterId=0):
        """
        Deletes an old litter
        """

        try:
            litterModel = Litter.objects.get(user=request.user, id=litterId)
        except Litter.DoesNotExist:
            errors = {'litterId': 'Litter id not found: ' + str(litterId)}
            returnData = {'errors': errors}
            return Response(returnData)

        litterModel.delete()
        returnData = {'status': 'okay'}
        return Response(returnData)


class LitterViewList(APIView):
    """
    View for multiple litter related requests

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        """
        Return all the litter a user has
        """
        litterModels = Litter.objects.filter(user=request.user)
        litterSerialized = LitterSerializer(litterModels, many=True)
        return Response(litterSerialized.data)

    def post(self, request, litterId=0):
        """
        Updates an old litter
        """
        serialized = LitterSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save(user=request.user)
            return Response(serialized.data)
        else:
            return Response(serialized.errors, status=400)
