from apps.my_auth.models import CustomUser
from rest_framework import serializers


def validate_players(data):
    userList = CustomUser.objects.filter(uuid=data)
    if userList.exists():
        return userList[0]
    else:
        raise serializers.ValidationError("User does not exist with that uuid.")