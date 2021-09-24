from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        module = CustomUser

    def validate_email(self, data):
        if CustomUser.objects.filter(email=data).exists():
            raise serializers.ValidationError('Email already in use.')
        return data


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        module = CustomUser


class CustomUserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'uuid']

    def to_representation(self, instance):
        from apps.games.models import Game
        rep = super().to_representation(instance)
        wins, losses = Game.objects.get_player_wins_losses(instance)
        rep['wins'] = wins
        rep['losses'] = losses
        return rep


# For updating a custom user
class CustomUserWriteSerializer(serializers.Serializer):
    class Meta:
        module = CustomUser

    email = serializers.EmailField()
    username = serializers.CharField()
    uuid = serializers.UUIDField()

    # Gotta be sure the new username doesn't exist already.
    def validate_username(self, data):
        if CustomUser.objects.filter(username=data).exists():
            # If the person is us, then whatever who cares
            if self.context.get('requester').username != data:
                raise serializers.ValidationError('Username is not available.')
        return data

    def validate(self, data):
        # Gotta make sure the person is the right person
        if self.context.get('requester').uuid != self.instance.uuid:
            raise serializers.ValidationError("Can't edit a user that isn't you.")
        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance

    def to_representation(self, instance):
        return CustomUserReadSerializer(instance).data
