from rest_framework import serializers

from apps.players.models import Player


def validate_players(data):
    userList = Player.objects.filter(uuid=data, is_staff=False)
    if not userList.exists():
        raise serializers.ValidationError("User does not exist with that uuid.")
