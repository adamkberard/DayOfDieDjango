from django.shortcuts import render

from apps.my_auth.serializers import CustomUserSerializer

from .models import Friend

# Create your views here.

class FriendView(APIView):
    """
    View to get all a person's friends

    * Requires token auth
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [authentication.TokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        friends = []
        friendSet = Friend.objects.filter()
        for game in gameSet:
            games.append(getGameJSON(game))

        return JsonResponse(data=games, status=201, safe=False)

    def post(self, request):
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
