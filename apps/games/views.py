from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Point
from .serializers import GameSerializer, PointSerializer
from apps.my_auth.models import CustomUser


class GameDetailView(APIView):
    """
    View for single game related requests

    * Requres token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request, pk):
        """
        Return a single game
        """
        try:
            gameModel = Game.objects.users_games(user=request.user).filter(id=pk)
            gamePoints  = Point.objects.filter(game=gameModel)
        except Game.DoesNotExist:
            errors = {'pk': 'Game id not found: ' + str(pk)}
            returnData = {'errors': errors}
            return Response(returnData)

        gameSerialized = GameSerializer(gameModel)
        pointsSerialized = PointSerializer(gamePoints, many=True)
        returnData = {'game': gameSerialized.data,
                      'points': pointsSerialized.data
                     }
        return Response(returnData)

    def put(self, request, pk):
        """
        Edits a game
        """
        #try:
        #    gameModel = Game.objects.get(user=request.user, id=pk)
        #    gamePoints  = Point.objects.filter(game=gameModel)
        #except Game.DoesNotExist:
        #    errors = {'pk': 'Game id not found: ' + str(pk)}
        #    returnData = {'errors': errors}
        #    return Response(returnData)

        #gameSerialized = GameSerializer(litterModel)
        #pointsSerialized = PointSerializer(litterModel, many=True)
        #returnData = {'game': gameSerialized,
        #              'points': pointsSerialized
        #             }
        returnData = {'error': 'hello world'}
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
        gamesSerialized = GameSerializer(gamesSet, many=True)
        return Response(data=gamesSerialized.data, status=201)

    def post(self, request):
        if 'game' not in request.data:
            data = {'game': ['This field is required.']}
            return Response(data=data, status=400)
        # We have to convert the incoming usernames into their pk's
        convertedGameData = convertToPK(request.data['game'])
        pointsData = request.data['points']
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
                point = serializedPoint.save()
                point.game = game
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
      

@csrf_exempt
def gameStats(request):
    playersData = []
    players = {"Adam", "Ben", "Jake", "Kyle", "Marcus"}
    for player in players:
        playerData = {}
        singlePoints = Point.objects.filter(scorer=player, typeOfPoint="PT").count
        tinks = Point.objects.filter(scorer=player, typeOfPoint="TK").count
        sinks = Point.objects.filter(scorer=player, typeOfPoint="SK").count
        bounceSinks = Point.objects.filter(scorer=player, typeOfPoint="BS").count
        partnerSinks = Point.objects.filter(scorer=player, typeOfPoint="PS").count
        selfSinks = Point.objects.filter(scorer=player, typeOfPoint="SS").count
        #total = singlePoints + (2 * (tinks + bounceSinks)) + (3 * sinks)
        playerData['name'] = player
        #playerData['totalPoints'] = total
        playerData['singlePoints'] = singlePoints
        playerData['tinks'] = tinks
        playerData['sinks'] = sinks
        playerData['bounceSinks'] = bounceSinks
        playerData['partnerSinks'] = partnerSinks
        playerData['selfSinks'] = selfSinks
        playersData.append(playerData)
    context = {}
    context['playersData'] = playersData
    return render(request, 'games/stats.html', context)
