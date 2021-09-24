from rest_framework import serializers

from apps.my_auth.models import CustomUser


def validate_players(data):
    userList = CustomUser.objects.filter(uuid=data)
    if not userList.exists():
        raise serializers.ValidationError("User does not exist with that uuid.")
