import string

from rest_framework import serializers

from apps.players.models import Player


class PlayerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['username', 'uuid']

    def to_representation(self, instance):
        from apps.games.models import Game
        rep = super().to_representation(instance)
        wins, losses = Game.objects.get_player_wins_losses(instance)
        rep['wins'] = wins
        rep['losses'] = losses
        return rep


# For updating a custom user
class PlayerWriteSerializer(serializers.Serializer):
    class Meta:
        module = Player

    email = serializers.EmailField()
    username = serializers.CharField()
    uuid = serializers.UUIDField()

    def checkUsernameContents(self, username):
        allowedCharacters = string.ascii_letters + string.digits
        allowedCharacters += ".-_"
        for character in username:
            if character not in allowedCharacters:
                raise serializers.ValidationError('Username may only contain A-z, 0-9, and .-_')

    # Gotta be sure the new username doesn't exist already.
    def validate_username(self, data):
        self.checkUsernameContents(data)
        if Player.objects.filter(username=data).exists():
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
        return Player.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance

    def to_representation(self, instance):
        return PlayerReadSerializer(instance).data
