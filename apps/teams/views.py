from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.my_auth.models import CustomUser

from .models import Team
from .serializers import TeamSerializer


class TeamDetailView(APIView):
    """
    View for single team related requests

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request, teamId):
        """
        Return a single team
        """
        try:
            usersTeamModels = Team.objects.users_teams(user=request.user)
            teamModel = usersTeamModels.get(id=teamId)
        except Team.DoesNotExist:
            returnData = {'teamId': ['Team id not found: ' + str(teamId)]}
            return Response(returnData, status=400)

        teamSerialized = TeamSerializer(teamModel)
        returnData = {'team': teamSerialized.data}
        return Response(returnData, status=200)

    def put(self, request, teamId):
        """
        Edits a single team
        """
        try:
            usersTeamModels = Team.objects.users_teams(user=request.user)
            teamModel = usersTeamModels.get(id=teamId)
        except Team.DoesNotExist:
            returnData = {'teamId': ['Team id not found: ' + str(teamId)]}
            return Response(returnData, status=400)

        if 'status' in request.data:
            if request.data['status'] == 'accept':
                # They can only accept it if they are the teammate
                if request.user == teamModel.teamCaptain:
                    estr = 'Cannot accept a team request as the teamCaptain.'
                    return Response({'errors': [estr]}, status=400)
                else:
                    teamModel.status = teamModel.ACCEPTED
                    teamModel.save()
            elif request.data['status'] == 'deny':
                if request.user == teamModel.teamCaptain:
                    estr = 'Cannot deny a team request as the teamCaptain.'
                    return Response({'errors': [estr]}, status=400)
                else:
                    teamModel.status = teamModel.DENIED
                    teamModel.save()

        teamSerialized = TeamSerializer(teamModel)
        returnData = {'team': teamSerialized.data}
        return Response(returnData, status=200)

    def delete(self, request, teamId):
        """
        Deletes a team
        """
        try:
            usersTeamModels = Team.objects.users_teams(user=request.user)
            teamModel = usersTeamModels.get(id=teamId)
        except Team.DoesNotExist:
            returnData = {'teamId': ['Team id not found: ' + str(teamId)]}
            return Response(returnData, status=400)

        teamModel.delete()
        return Response(status=200)


class TeamView(APIView):
    """
    View for getting all lists, and posting

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        usersTeamModels = Team.objects.users_teams(user=request.user)

        teamsSerialized = TeamSerializer(usersTeamModels, many=True)
        myOwnData = []
        for temp in teamsSerialized.data:
            myOwnData.append(temp)

        for teamData in myOwnData:
            for field in teamData:
                if field == 'teamCaptain':
                    if teamData['teamCaptain'] == request.user.username:
                        teamData['partner'] = teamData['teammate']
                        teamData.pop('teamCaptain', None)
                        teamData.pop('teammate', None)
                        break
                if field == 'teammate':
                    if teamData['teammate'] == request.user.username:
                        teamData['partner'] = teamData['teamCaptain']
                        teamData.pop('teamCaptain', None)
                        teamData.pop('teammate', None)
                        break

        returnData = {'teams': myOwnData}
        return Response(returnData, status=200)

    def post(self, request):
        """Posting a new team. Pretty simple stuff"""
        if 'teammate' not in request.data:
            data = {'teammate': ['This field is required.']}
            return Response(data=data, status=400)

        # Making sure the incoming team exists
        usrname = request.data['teammate']
        try:
            teamModel = CustomUser.objects.get(username=usrname)
        except CustomUser.DoesNotExist:
            estr = 'Cannot find a user with username: {}'.format(usrname)
            returnData = {'errors': [estr]}
            return Response(returnData, status=400)

        # Creating teamship, default is pending so that works out
        teamshipModel = Team(teamCaptain=request.user, teammate=teamModel)
        teamshipModel.save()
        teamshipSerialized = TeamSerializer(teamshipModel)

        returnData = {'team': teamshipSerialized.data}
        return Response(returnData, status=201)
