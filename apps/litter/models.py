from django.conf import settings
from django.db import models


class Litter(models.Model):
    INDIVIDUAL_PIECE = 'IND'
    GROCERY_BAG = 'GRO'
    GARBAGE_BAG = 'GAR'
    LITTER_TYPE_CHOICES = [
        (INDIVIDUAL_PIECE, 'individual piece of litter'),
        (GROCERY_BAG, 'grocery bag of litter'),
        (GARBAGE_BAG, 'garbage bag of litter'),
    ]

    typeOfLitter = models.CharField(max_length=3,
                                    choices=LITTER_TYPE_CHOICES,
                                    default=INDIVIDUAL_PIECE)

    amount = models.IntegerField()
    timeCollected = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def create(self, validated_data):
        return Litter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.typeOfLitter = validated_data.get('typeOfLitter',
                                                   instance.typeOfLitter)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.timeCollected = validated_data.get('timeCollected',
                                                    instance.timeCollected)
        instance.save()
        return instance
