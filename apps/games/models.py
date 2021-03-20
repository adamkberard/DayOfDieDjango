from django.conf import settings
from django.db import models

from .managers import GameManager


class GameSettings(models.Model):
    # Settings for games
    numPointsToWin = models.IntegerField()
    singlePointsValue = models.IntegerField()
    tinkPointsValue = models.IntegerField()
    sinkPointsValue = models.IntegerField()
    bounceSinkPointsValue = models.IntegerField()
    partnerSinkPointsValue = models.IntegerField()
    selfSinkPointsValue = models.IntegerField()
    winByTwo = models.BooleanField()


# Create your models here.
class Game(models.Model):
    timeStarted = models.DateTimeField()
    timeSaved = models.DateTimeField()
    playerOne = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name="p1")
    playerTwo = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name="p2")
    playerThree = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name="p3")
    playerFour = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name="p4")

    objects = GameManager()

    def __str__(self):
        return str(self.timeSaved)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timeSaved = validated_data.get('timeSaved',
                                                instance.timeSaved)
        instance.playerOne = validated_data.get('playerOne',
                                                instance.playerOne)
        instance.playerTwo = validated_data.get('playerTwo',
                                                instance.playerTwo)
        instance.playerThree = validated_data.get('playerThree',
                                                  instance.playerThree)
        instance.playerFour = validated_data.get('playerFour',
                                                 instance.playerFour)
        instance.save()
        return instance


class Point(models.Model):
    SINGLE_POINT = 'PT'
    TINK = 'TK'
    SINK = 'SK'
    BOUNCE_SINK = 'BS'
    PARTNER_SINK = 'PS'
    SELF_SINK = 'SS'

    SCORED_POINT_CHOICES = [
        (SINGLE_POINT, 'regular point'),
        (SELF_SINK, 'self sink'),
    ]

    SCORED_ON_POINT_CHOICES = [
        (TINK, 'tink'),
        (SINK, 'sink'),
        (BOUNCE_SINK, 'bounce sink'),
        (PARTNER_SINK, 'partner sink'),
    ]

    POINT_TYPE_CHOICES = SCORED_POINT_CHOICES + SCORED_ON_POINT_CHOICES

    typeOfPoint = models.CharField(max_length=2,
                                   choices=POINT_TYPE_CHOICES,
                                   default=SINGLE_POINT)

    scorer = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    scoredOn = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='scored',
                                 null=True, blank=True)

    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             null=True, blank=True,
                             related_name='scoredOn')

    def __str__(self):
        if self.typeOfPoint == 'PT':
            return "{} scored".format(self.scorer)
        elif self.typeOfPoint == "TK":
            return "{} tinked {}".format(self.scorer, self.scoredOn)
        elif self.typeOfPoint == "SK":
            return "{} sank {}".format(self.scorer, self.scoredOn)
        elif self.typeOfPoint == "BS":
            return "{} bounce sank {}".format(self.scorer, self.scoredOn)
        elif self.typeOfPoint == "PS":
            return "{} sank their partner, {}".format(self.scorer,
                                                      self.scoredOn)
        elif self.typeOfPoint == "SS":
            return "{} self sank".format(self.scorer)
        return "You shouldn't be seeing this."

    def create(self, validated_data):
        return Point.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.typeOfPoint = validated_data.get('typeOfPoint',
                                                  instance.typeOfPoint)
        instance.scorer = validated_data.get('scorer', instance.scorer)
        instance.scoredOn = validated_data.get('scoredOn',
                                               instance.scoredOn)
        instance.game = validated_data.get('game', instance.game)
        instance.save()
        return instance
