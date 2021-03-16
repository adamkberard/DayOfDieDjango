from rest_framework import serializers

from tools.ids_encoder.converters import HashidsConverter

from apps.my_auth.serializers import CustomUserSerializer
from apps.my_auth.models import CustomUser

from .models import Game, Point


class PointSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Point
        fields = '__all__'

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

    def to_representation(self, instance):
        """
        Changes the id to hashed id before it sends it out
        """
        ret = super().to_representation(instance)
        converter = HashidsConverter()
        if ret['id'] is not None:
            ret['id'] = converter.to_url(ret['id'])
        if ret['game'] is not None:
            ret['game'] = converter.to_url(ret['game'])

        # Changes the player id's to their usernames
        players = ['scorer', 'scoredOn']

        for player in players:
            if ret[player] is not None:
                playerId = ret[player]
                ret[player] = CustomUser.objects.get(id=playerId).username
        return ret


class GameSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        game = Game.objects.create(**validated_data)
        return game

    def update(self, instance, validated_data):
        instance.timeStarted = validated_data.get('timeStarted', instance.timeStarted)
        instance.timeSaved = validated_data.get('timeSaved', instance.timeSaved)
        instance.playerOne = validated_data.get('playerOne', instance.playerOne)
        instance.playerTwo = validated_data.get('playerTwo', instance.playerTwo)
        instance.playerThree = validated_data.get('playerThree', instance.playerThree)
        instance.playerFour = validated_data.get('playerFour', instance.playerFour)
        instance.save()

        return instance

    def to_representation(self, instance):
        """
        Changes the id to hashed id before it sends it out
        """
        ret = super().to_representation(instance)
        converter = HashidsConverter()
        if ret['id'] is not None:
            ret['id'] = converter.to_url(ret['id'])

        # Changes the player id's to their usernames
        players = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']

        for player in players:
            if ret[player] is not None:
                playerId = ret[player]
                ret[player] = CustomUser.objects.get(id=playerId).username
        return ret
