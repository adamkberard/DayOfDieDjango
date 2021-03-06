from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.forms.models import model_to_dict

from .models import Game, Point

@csrf_exempt
def gameCRUD(request):
    """
    Creates a new game and all the points
    """
    if request.method == 'GET':
        games = []
        gameSet = Game.objects.all()
        for game in gameSet:
            games.append(getGameJSON(game))

        return JsonResponse(data=games, status=201, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)

        gameDict = data['game']
        pointDicts = gameDict['points']

        # Gets the game data and creates and saves a game
        game = Game()
        game.playerOne = gameDict['playerOne']
        game.playerTwo = gameDict['playerTwo']
        game.playerThree = gameDict['playerThree']
        game.playerFour = gameDict['playerFour']
        game.save()
        
        # Creates all the different points
        for pointDict in pointDicts:
            tempPoint = Point()
            tempPoint.typeOfPoint = pointDict['typeOfPoint']
            tempPoint.scorer = pointDict['scorer']
            tempPoint.scoredOn = pointDict['scoredOn']
            tempPoint.game = game
            tempPoint.save()

        return JsonResponse(data={'status': 'okay'}, status=201)

@csrf_exempt
def gameCRUDDetail(request, gameId):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

def getGameJSON(game):
    pointsSet = Point.objects.filter(game=game)
    
    points = []

    for point in pointsSet:
        points.append(model_to_dict(point))

    return {'game': model_to_dict(game), 'points': points}

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
        total = singlePoints
        total += int(2 * tinks)
        total += 2 * bounceSinks
        total += 3 * sinks
        playerData['name'] = player
        playerData['totalPoints'] = total
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
    return 
