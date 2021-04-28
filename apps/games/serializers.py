from rest_framework import serializers

from apps.friends.serializers import FriendSerializer
from apps.my_auth.serializers import BasicCustomUserSerializer
from apps.my_auth.models import CustomUser
from apps.friends.models import Friend

from .models import Game, Point


class PointSerializer(serializers.ModelSerializer):

    scorer = BasicCustomUserSerializer() 
    scored_on = BasicCustomUserSerializer(read_only=True) 

    class Meta:
        model = Point
        exclude = ['id', 'created', 'modified', 'game']

    # I want the return for the game to be the UUID
    # I may not even need to send this idk.
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['game'] = instance.game.uuid
        return representation


class GameSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Game
        fields = ('time_started', 'time_ended', 'uuid', 'type', 'team_one', 'team_two', 
                  'team_one_score', 'team_two_score', 'confirmed', 'points')
        extra_kwargs = {
            'points': {'write_only': True}
        }

    team_one = FriendSerializer()
    team_two = FriendSerializer()

    def to_representation(self, instance):
        instance.points = []
        representation = super().to_representation(instance)
        points_set = Point.objects.filter(game=instance)
        serialized_points = PointSerializer(points_set, many=True)
        representation['points'] = serialized_points.data
        return representation

    def create(self, validated_data):
        points_data = validated_data.pop('points')
        # Must find the teams myself, if they don't exist I create them
        team_one_data = validated_data.pop('team_one')
        team_one_team_captain = CustomUser.objects.get(uuid=team_one_data['team_captain']['uuid'])
        team_one_teammate = CustomUser.objects.get(uuid=team_one_data['teammate']['uuid'])

        team_two_data = validated_data.pop('team_two')
        team_two_team_captain = CustomUser.objects.get(uuid=team_two_data['team_captain']['uuid'])
        team_two_teammate = CustomUser.objects.get(uuid=team_two_data['teammate']['uuid'])

        team_one = Friend.objects.get_or_create_friend(team_one_team_captain, team_one_teammate)
        team_two = Friend.objects.get_or_create_friend(team_two_team_captain, team_two_teammate)

        game = Game.objects.create(**validated_data, team_one=team_one, team_two=team_two)

        for point_data in points_data:
            scorer = CustomUser.objects.get(uuid=point_data.pop('scorer')['uuid'])
            scored_on_uuid = point_data.pop('scored_on', None)
            if scored_on_uuid:
                scored_on = CustomUser.objects.get(uuid=scored_on_uuid)
            else:
                scored_on = None
            Point.objects.create(game=game, scorer=scorer, scored_on=scored_on, **point_data)

        return game
