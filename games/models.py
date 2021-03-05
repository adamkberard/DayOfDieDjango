from django.conf import settings
from django.db import models

# Create your models here.
class Game(models.Model):
    timeSaved = models.DateTimeField(auto_now_add=True)
    playerOne = models.CharField(max_length=30)
    playerTwo = models.CharField(max_length=30)
    playerThree = models.CharField(max_length=30)
    playerFour = models.CharField(max_length=30)

    def __str__(self):
        return str(self.timeSaved)

class Point(models.Model):
    SINGLE_POINT = 'PT'
    TINK = 'TK'
    SINK = 'SK'
    BOUNCE_SINK = 'BS'
    PARTNER_SINK = 'PS'
    SELF_SINK = 'SS'

    POINT_TYPE_CHOICES = [
        (SINGLE_POINT, 'regular point'),
        (TINK, 'tink'),
        (SINK, 'sink'),
        (BOUNCE_SINK, 'bounce sink'),
        (PARTNER_SINK, 'partner sink'),
        (SELF_SINK, 'self sink'),
    ]

    typeOfPoint = models.CharField(max_length=2,
                                   choices=POINT_TYPE_CHOICES,
                                   default=SINGLE_POINT)
    scorer = models.CharField(max_length=30)
    scoredOn = models.CharField(max_length=30, blank=True, null=True)

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return "{} scored a {} on {}".format(self.scorer, self.typeOfPoint, self.scoredOn)

    #def create(self, validated_data):
    #    return Litter.objects.create(**validated_data)

    #def update(self, instance, validated_data):
    #    instance.typeOfLitter = validated_data.get('typeOfLitter',
    #                                               instance.typeOfLitter)
    #    instance.amount = validated_data.get('amount', instance.amount)
    #    instance.timeCollected = validated_data.get('timeCollected',
    #                                                instance.timeCollected)
    #    instance.save()
    #    return instance
