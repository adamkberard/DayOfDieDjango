from apps.players.serializers import PlayerReadSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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

    def create(self, validated_data):
        user = Player.objects.create_user(email=validated_data['email'],
                                          password=validated_data['password'])
        return user
    
    def to_representation(self, instance):
        return LogInSerializer(instance).data


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        module = Player

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Not a valid user.')
        return data

    def create(self, validated_data):
        user = authenticate(username=validated_data['email'], password=validated_data['password'])
        return user

    def to_representation(self, instance):
        token, _ = Token.objects.get_or_create(user=instance)
        data = {
            'token': str(token),
            'player': PlayerReadSerializer(instance).data
        }
        return data
