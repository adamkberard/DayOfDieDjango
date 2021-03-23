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
            returnData = {'error': 'Team id not found: ' + str(teamId)}
            return Response(returnData)

        teamSerialized = TeamSerializer(teamModel)
        returnData = {'team': teamSerialized.data}
        return Response(returnData)

    def put(self, request, teamId):
        """
        Edits a single team
        """
        try:
            usersTeamModels = Team.objects.users_teams(user=request.user)
            teamModel = usersTeamModels.get(id=teamId)
        except Team.DoesNotExist:
            returnData = {'error': 'Team id not found: ' + str(teamId)}
            return Response(returnData)

        if 'status' in request.data:
            if request.data['status'] == 'accept':
                # They can only accept it if they are the teammate
                if request.user == teamModel.teamCaptain:
                    errStr = 'Cannot accept a team request as the teamCaptain.'
                    return Response({'error': errStr})
                else:
                    teamModel.status = teamModel.ACCEPTED
                    teamModel.save()
            elif request.data['status'] == 'deny':
                if request.user == teamModel.teamCaptain:
                    errStr = 'Cannot deny a team request as the teamCaptain.'
                    return Response({'error': errStr})
                else:
                    teamModel.status = teamModel.DENIED
                    teamModel.save()

        teamSerialized = TeamSerializer(teamModel)
        returnData = {'team': teamSerialized.data}
        return Response(returnData)

    def delete(self, request, teamId):
        """
        Deletes a team
        """
        try:
            usersTeamModels = Team.objects.users_teams(user=request.user)
            teamModel = usersTeamModels.get(id=teamId)
        except Team.DoesNotExist:
            returnData = {'error': 'Team id not found: ' + str(teamId)}
            return Response(returnData)

        teamModel.delete()
        returnData = {'status': 'okay'}
        return Response(returnData)


class TeamView(APIView):
    """
    View for getting all lists, and posting

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            usersTeamModels = Team.objects.users_teams(user=request.user)
        except Team.DoesNotExist:
            returnData = {'error': 'Team id not found: '}
            return Response(returnData)

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
        return Response(returnData)

    def post(self, request):
        """Posting a new team. Pretty simple stuff"""
        if 'team' not in request.data:
            data = {'team': ['This field is required.']}
            return Response(data=data, status=400)

        # Making sure the incoming team exists
        usrname = request.data['team']
        try:
            teamModel = CustomUser.objects.get(username=usrname)
        except CustomUser.DoesNotExist:
            errStr = 'Cannot find a user with username: {}'.format(usrname)
            returnData = {'error': errStr}
            return Response(returnData)

        # Creating teamship, default is pending so that works out
        teamshipModel = Team(teamCaptain=request.user, teammate=teamModel)
        teamshipModel.save()
        teamshipSerialized = TeamSerializer(teamshipModel)

        returnData = {'team': teamshipSerialized.data}
        return Response(returnData)
