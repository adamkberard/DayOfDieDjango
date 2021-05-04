from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import CustomUser
from apps.games.models import Game
from apps.friends.models import Friend


class MyRegisterSerializer(serializers.Serializer):
    class Meta:
        module = CustomUser

    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = {}

        # First we get the user that we know exists because of validation
        representation['user'] = CustomUserSerializer(instance).data

        # Gotta check if there's a token and create it if not
        # Then we send the token but in the user one cuz it's easier?
        token, _ = Token.objects.get_or_create(user=instance)
        representation['user']['token'] = str(token)

        representation['games'] = []
        representation['friends'] = []

        # All usernames in the system
        usernames = CustomUser.objects.all().values('username')
        formatted_usernames = []
        for username in usernames:
            formatted_usernames.append(username['username'])
        representation['all_usernames'] = formatted_usernames

        return representation


class MyLogInSerializer(serializers.Serializer):
    class Meta:
        module = CustomUser

    email = serializers.EmailField()
    password = serializers.CharField()

    def save(self, **kwargs):
        # I don't actually wanna save anything so I just return it. Not sure if this is a chill 
        # way to do it. Odds are there's a better way to login people, but until I find it this 
        # will suffice.
        return self.validated_data

    def validate(self, data):
        """
        Gotta makes sure the person can be logged in
        """
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Not a valid user.")
        return user

    def to_representation(self, instance):
        from apps.friends.serializers import FriendSerializer
        from apps.games.serializers import GameSerializer
        representation = {}

        # First we get the user that we know exists because of validation
        representation['user'] = CustomUserSerializer(instance).data

        # Gotta check if there's a token and create it if not
        # Then we send the token but in the user one cuz it's easier?
        token, _ = Token.objects.get_or_create(user=instance)
        representation['user']['token'] = str(token)

        # Now we get the games
        games = Game.objects.users_games(user=instance)
        representation['games'] = GameSerializer(games, many=True).data

        # Now we get the friends
        friends = Friend.objects.users_friends(user=instance)
        representation['friends'] = FriendSerializer(friends, many=True).data

        # All usernames in the system
        usernames = CustomUser.objects.all().values('username')
        formatted_usernames = []
        for username in usernames:
            formatted_usernames.append(username['username'])
        representation['all_usernames'] = formatted_usernames
        return representation


class CustomUserSerializer(serializers.Serializer):
    class Meta:
        module = CustomUser

    email = serializers.EmailField()
    username = serializers.CharField()
    uuid = serializers.UUIDField()

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        return instance


class BasicCustomUserSerializer(serializers.Serializer):
    class Meta:
        module = CustomUser

    username = serializers.CharField()
    uuid = serializers.UUIDField()
