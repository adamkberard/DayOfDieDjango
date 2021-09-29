from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.players.models import Player


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        module = Player

    def validate_email(self, data):
        if Player.objects.filter(email=data).exists():
            raise serializers.ValidationError('Email already in use.')
        return data


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        module = Player
