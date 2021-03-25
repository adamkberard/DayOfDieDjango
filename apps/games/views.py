from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tools.helperFunctions.helperFuncs import convertToPK

from .models import Game, Point
from .serializers import GameSerializer, PointSerializer


class GameDetailView(APIView):
    """
    View for single game related requests

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request, gameId):
        """
        Return a single game
        """
        try:
            usersGameModels = Game.objects.users_games(user=request.user)
            gameModel = usersGameModels.get(id=gameId)
            gamePoints = Point.objects.filter(game=gameModel)
        except Game.DoesNotExist:
            estr = 'Game id not found: {}'.format(gameId)
            returnData = {'gameId': [estr]}
            return Response(returnData, status=400)

        gameSerialized = GameSerializer(gameModel)
        pointsSerialized = PointSerializer(gamePoints, many=True)
        tempDict = gameSerialized.data
        tempDict['points'] = pointsSerialized.data
        return Response({'game': tempDict}, status=200)

    def put(self, request, gameId):
        """
        Edits a game
        """
        try:
            usersGameModels = Game.objects.users_games(user=request.user)
            gameModel = usersGameModels.get(id=gameId)
        except Game.DoesNotExist:
            estr = 'Game id not found: {}'.format(gameId)
            returnData = {'gameId': [estr]}
            return Response(returnData, status=400)

        # Updates the game and gets the serialized data or just gets the
        # serialized data. Throws errors if found either way
        if 'game' not in request.data:
            estr = 'This field is required.'
            returnData = {'game': [estr]}
            return Response(returnData, status=400)

        if 'points' not in request.data['game']:
            estr = 'This field is required.'
            returnData = {'game_points': [estr]}
            return Response(returnData, status=400)

        # First I have to take the id's and unhash them
        if 'id' in request.data['game']:
            convertedGame = convertToPK(request.data['game'])
        else:
            estr = 'This field is required.'
            returnData = {'game_id': [estr]}
            return Response(returnData, status=400)

        gameSerialized = GameSerializer(gameModel, data=convertedGame)
        if gameSerialized.is_valid():
            gameModel = gameSerialized.save()
        else:
            return Response(gameSerialized.errors, status=400)

        unsavedPoints = []
        for pointData in request.data['game']['points']:
            convertedPoint = convertToPK(pointData)
            convertedPoint['game'] = gameModel.id
            serializedPoint = PointSerializer(data=convertedPoint)
            if serializedPoint.is_valid():
                unsavedPoints.append(serializedPoint)
            else:
                return Response(serializedPoint.errors, status=400)

        # If everything goes right I delete the previous points
        Point.objects.filter(game=gameModel).delete()

        # Then I save all the points I just serialized
        for unsavedPoint in unsavedPoints:
            unsavedPoint.save(game=gameModel)

        gameSerialized = GameSerializer(gameModel)
        pointModels = Point.objects.filter(game=gameModel)
        pointsSerialized = PointSerializer(pointModels, many=True)

        tempDict = gameSerialized.data
        tempDict['points'] = pointsSerialized.data
        returnData = {'game': tempDict}
        return Response(returnData, status=200)

    def delete(self, request, gameId):
        """
        Deletes a game
        """
        try:
            usersGameModels = Game.objects.users_games(user=request.user)
            gameModel = usersGameModels.get(id=gameId)
        except Game.DoesNotExist:
            estr = 'Game id not found: {}'.format(gameId)
            returnData = {'gameId': [estr]}
            return Response(returnData, status=400)

        # Delete the points
        Point.objects.filter(game=gameModel).delete()

        # Delete the game
        Game.objects.get(id=gameModel.id).delete()

        return Response(status=200)


class GameView(APIView):
    """
    View for getting all lists, and posting

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        gamesSet = Game.objects.users_games(user=request.user)
        returnData = []
        for game in gamesSet:
            gamePoints = Point.objects.filter(game=game)

            gameSerialized = GameSerializer(game)
            pointsSerialized = PointSerializer(gamePoints, many=True)

            tempDict = gameSerialized.data
            tempDict['points'] = pointsSerialized.data
            returnData.append({'game': tempDict})

        return Response(data={'games': returnData}, status=200)

    def post(self, request):
        # Since I'm doing more than one object at a time, I have to also
        # check for to be sure the things exist
        edict = {}
        if 'game' not in request.data:
            edict['game'] = ['This field is required.']
            return edict
        if 'points' not in request.data['game']:
            edict['points'] = ['This field is required in game.']

        if len(edict) != 0:
            return Response(data=edict, status=400)

        # We have to convert the incoming usernames into their pk's
        convertedGameData = convertToPK(request.data['game'])
        serializedGame = GameSerializer(data=convertedGameData)

        points = []

        if serializedGame.is_valid():
            game = serializedGame.save()
        else:
            return Response(data=serializedGame.errors, status=400)

        for pointData in request.data['game']['points']:
            convertedPoint = convertToPK(pointData)
            serializedPoint = PointSerializer(data=convertedPoint)
            if serializedPoint.is_valid():
                serializedPoint.save(game=game)
                points.append(serializedPoint.data)
            else:
                edict.update(serializedPoint.errors)

        if len(edict) != 0:
            return Response(data=edict, status=400)
        else:
            tempDict = serializedGame.data
            tempDict['points'] = points
            returnData = {'game': tempDict}
            return Response(data=returnData, status=201)
