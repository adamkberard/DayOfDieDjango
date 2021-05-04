from rest_framework import serializers

from apps.my_auth.serializers import BasicCustomUserSerializer

from .models import Friend
from apps.my_auth.models import CustomUser


class FriendSerializer(serializers.ModelSerializer):
    team_captain = BasicCustomUserSerializer()
    teammate = BasicCustomUserSerializer()

    class Meta:
        model = Friend
        exclude = ['id', 'created', 'modified']

    def validate(self, data):
        """
        Makes sure the friends is okay
        """
        # This is making sure the two users are different
        if data['team_captain'] == data['teammate']:
            raise serializers.ValidationError("Users must be different.")
        return data


class FriendCreateSerializer(serializers.ModelSerializer):
    team_captain = serializers.CharField()
    teammate = serializers.CharField()

    class Meta:
        model = Friend
        fields = ['team_captain', 'teammate', 'status']

    def create(self, validated_data):
        # First I will check if a friend request already exists
        team_captain = CustomUser.objects.get(username=validated_data['team_captain'])
        teammate = CustomUser.objects.get(username=validated_data['teammate'])

        friend = Friend.objects.get_or_create_friend(team_captain, teammate)

        # Check to make sure it's the teammate answering the request
        if friend.status == friend.STATUS_NOTHING:
            if validated_data['status'] == 'ac':
                friend.team_captain = team_captain
                friend.teammate = teammate
                friend.status = friend.STATUS_PENDING
        elif friend.status == friend.STATUS_PENDING:
            if team_captain == friend.teammate:
                if validated_data['status'] == friend.STATUS_DENIED:
                    friend.status = friend.STATUS_DENIED
                elif validated_data['status'] == friend.STATUS_ACCEPTED:
                    friend.status = friend.STATUS_ACCEPTED
            else:
                if validated_data['status'] == 'dn':
                    print("GOT HERE")
                    friend.status = friend.STATUS_NOTHING

        friend.save()
        print(friend.status)
        return friend

    def validate_action(self, value):
        if value not in ['ac', 'dn']:
            raise serializers.ValidationError('Action not valid.')

    def validate(self, data):
        """
        Makes sure the friends is okay
        """
        # This is making sure the two users are different
        if data['team_captain'] == data['teammate']:
            raise serializers.ValidationError("Users must be different.")
        return data

    def to_representation(self, instance):
        return FriendSerializer(instance).data
