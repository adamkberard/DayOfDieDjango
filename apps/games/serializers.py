from rest_framework import serializers

from apps.friends.models import Friend
from apps.friends.serializers import FriendSerializer
from apps.my_auth.models import CustomUser
from apps.my_auth.serializers import CustomUserReadSerializer

from .models import Game, Point


class PointWriteSerializer(serializers.Serializer):
    scorer = serializers.UUIDField()
    type = serializers.ChoiceField(choices=[x[0] for x in Point.TYPE_CHOICES])


class GameWriteSerializer(serializers.Serializer):
    playerOne = serializers.UUIDField()
    playerTwo = serializers.UUIDField()
    playerThree = serializers.UUIDField()
    playerFour = serializers.UUIDField()

    team_one_score = serializers.IntegerField()
    team_two_score = serializers.IntegerField()

    time_started = serializers.DateTimeField()
    time_ended = serializers.DateTimeField()

    points = PointWriteSerializer(many=True)

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

        _, team_one = Friend.objects.get_or_create_friend(playerOne, playerTwo)
        _, team_two = Friend.objects.get_or_create_friend(playerThree, playerFour)

        team_one.save()
        team_two.save()

        # Created games are always unconfirmed
        game = Game.objects.create(**validated_data, team_one=team_one,
                                   team_two=team_two, confirmed=False)

        for point_data in points_data:
            scorer = CustomUser.objects.get(uuid=point_data.get('scorer'))
            type = point_data.get('type')
            Point.objects.create(game=game, scorer=scorer, type=type)

        return game


class PointSerializer(serializers.ModelSerializer):
    scorer = CustomUserReadSerializer()

    class Meta:
        model = Point
        exclude = ['created', 'modified', 'game']


class GameSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    team_one = FriendSerializer()
    team_two = FriendSerializer()

    class Meta:
        model = Game
        exclude = ['created', 'modified']

    def to_representation(self, instance):
        instance.points = []
        representation = super().to_representation(instance)
        points_set = Point.objects.filter(game=instance)
        serialized_points = PointSerializer(points_set, many=True)
        representation['points'] = serialized_points.data
        return representation
