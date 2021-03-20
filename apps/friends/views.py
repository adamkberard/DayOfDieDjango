# from rest_framework import authentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.renderers import JSONRenderer
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from apps.my_auth.models import CustomUser
# from .models import Friend


# class FriendView(APIView):
#     """
#     View to get all a person's friends
#
#     * Requires token auth
#     """
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = [authentication.TokenAuthentication]
#     renderer_classes = [JSONRenderer]
