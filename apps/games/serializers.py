from rest_framework import serializers

from apps.friends.serializers import FriendSerializer
from apps.my_auth.serializers import BasicCustomUserSerializer
from apps.my_auth.models import CustomUser
from apps.friends.models import Friend

from .models import Game, Point


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        exclude = ['id', 'created', 'modified', 'game']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class GameSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    team_one = FriendSerializer()
    team_two = FriendSerializer()

    class Meta:
        model = Game
        exclude = ['id', 'created', 'modified']


    def to_representation(self, instance):
        instance.points = []
        representation = super().to_representation(instance)
        points_set = Point.objects.filter(game=instance)
        serialized_points = PointSerializer(points_set, many=True)
        representation['points'] = serialized_points.data
        return representation


class GameWriteSerializer(serializers.Serializer):
    playerOne = serializers.UUIDField()
    playerTwo = serializers.UUIDField()
    playerThree = serializers.UUIDField()
    playerFour = serializers.UUIDField()

    team_one_score = serializers.IntegerField()
    team_two_score = serializers.IntegerField()

    time_started = serializers.DateTimeField()
    time_ended = serializers.DateTimeField()

    points = PointSerializer(many=True)

    def to_representation(self, instance):
        rep = GameSerializer(instance).data
        return rep

    def create(self, validated_data):
        points_data = validated_data.pop('points')

        # Must find the teams myself, if they don't exist I create them
        playerOne = CustomUser.objects.get(uuid=validated_data.pop('playerOne'))
        playerTwo = CustomUser.objects.get(uuid=validated_data.pop('playerTwo'))
        playerThree = CustomUser.objects.get(uuid=validated_data.pop('playerThree'))
        playerFour = CustomUser.objects.get(uuid=validated_data.pop('playerFour'))

        team_one = Friend.objects.get_or_create_friend(playerOne, playerTwo)
        team_two = Friend.objects.get_or_create_friend(playerThree, playerFour)

        # Created games are always unconfirmed
        game = Game.objects.create(**validated_data, team_one=team_one, team_two=team_two, confirmed=False)

        for point_data in points_data:
            scorer = CustomUser.objects.get(uuid=point_data.pop('scorer')['uuid'])
            scored_on_uuid = point_data.pop('scored_on', None)
            if scored_on_uuid:
                scored_on = CustomUser.objects.get(uuid=scored_on_uuid)
            else:
                scored_on = None
            Point.objects.create(game=game, scorer=scorer, scored_on=scored_on, **point_data)

        return game
