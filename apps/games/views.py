from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.my_auth.models import CustomUser

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
            returnData = {'error': 'Game id not found: ' + str(gameId)}
            return Response(returnData)

        gameSerialized = GameSerializer(gameModel)
        pointsSerialized = PointSerializer(gamePoints, many=True)
        returnData = {'game': gameSerialized.data,
                      'points': pointsSerialized.data}
        return Response(returnData)

    def put(self, request, gameId):
        """
        Edits a game
        """
        try:
            usersGameModels = Game.objects.users_games(user=request.user)
            gameModel = usersGameModels.get(id=gameId)
        except Game.DoesNotExist:
            returnData = {'error': 'Game id not found: ' + str(gameId)}
            return Response(returnData)

        # Updates the game and gets the serialized data or just gets the
        # serialized data. Throws errors if found either way
        if 'game' in request.data:
            # First I have to take the id's and unhash them
            request.data['id'] = gameId
            convertedGame = convertToPK(request.data['game'])

            gameSerialized = GameSerializer(gameModel, data=convertedGame)
            if gameSerialized.is_valid():
                gameModel = gameSerialized.save()
            else:
                return Response(gameSerialized.errors, status=400)

        # Deletes old points and saves new ones
        # Gets the serialized data or just gets the serialized data. Throws
        # errors if found either way
        if 'points' in request.data:
            unsavedPoints = []

            for pointData in request.data['points']:
                convertedPoint = convertToPK(pointData)
                convertedPoint['game'] = gameModel.id
                serializedPoint = PointSerializer(data=convertedPoint)
                if serializedPoint.is_valid():
                    unsavedPoints.append(serializedPoint)
                else:
                    return Response(serializedPoint.errors)

            # If everything goes right I delete the previous points
            Point.objects.filter(game=gameModel).delete()

            # Then I save all the points I just serialized
            for unsavedPoint in unsavedPoints:
                unsavedPoint.save(game=gameModel)

        gameSerialized = GameSerializer(gameModel)
        pointModels = Point.objects.filter(game=gameModel)
        pointsSerialized = PointSerializer(pointModels, many=True)

        returnData = {'game': gameSerialized.data,
                      'points': pointsSerialized.data}
        return Response(returnData)

    def delete(self, request, gameId):
        """
        Deletes a game
        """
        try:
            usersGameModels = Game.objects.users_games(user=request.user)
            gameModel = usersGameModels.get(id=gameId)
        except Game.DoesNotExist:
            returnData = {'error': 'Game id not found: ' + str(gameId)}
            return Response(returnData)

        # Delete the points
        Point.objects.filter(game=gameModel)

        # Delete the game
        Game.objects.get(id=gameModel.id).delete()

        returnData = {'status': 'okay'}
        return Response(returnData)


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
            pointsSet = Point.objects.filter(game=game)
            pointsSerialized = PointSerializer(pointsSet, many=True)
            gameSerialized = GameSerializer(game)
            gameDict = {'game': gameSerialized.data,
                        'points': pointsSerialized.data}
            returnData.append(gameDict)
        return Response(data=returnData, status=201)

    def post(self, request):
        # Since I'm doing more than one object at a time, I have to also
        # check for to be sure the things exist
        if 'game' not in request.data:
            data = {'game': ['This field is required.']}
            return Response(data=data, status=400)
        if 'points' not in request.data:
            data = {'points': ['This field is required.']}
            return Response(data=data, status=400)
        # We have to convert the incoming usernames into their pk's
        convertedGameData = convertToPK(request.data['game'])
        serializedGame = GameSerializer(data=convertedGameData)

        errors = {}
        points = []

        if serializedGame.is_valid():
            game = serializedGame.save()
        else:
            return Response(data=serializedGame.errors)

        for pointData in request.data['points']:
            convertedPoint = convertToPK(pointData)
            serializedPoint = PointSerializer(data=convertedPoint)
            if serializedPoint.is_valid():
                serializedPoint.save(game=game)
                points.append(serializedPoint.data)
            else:
                errors.update(serializedPoint.errors)

        if len(errors) == 0:
            returnData = {'game': serializedGame.data,
                          'points': points}
            return Response(data=returnData)
        else:
            return Response(data=errors)


def convertToPK(data):
    terms = ['playerOne', 'playerTwo', 'playerThree', 'playerFour',
             'scorer', 'scoredOn']

    for term in terms:
        if term in data:
            username = data[term]
            if username is not None:
                data[term] = CustomUser.objects.get(username=username).id

    return data
