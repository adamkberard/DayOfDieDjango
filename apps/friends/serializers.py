from rest_framework import serializers

from apps.my_auth.serializers import BasicCustomUserSerializer

from .models import Friend


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
