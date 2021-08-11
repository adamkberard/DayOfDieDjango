from rest_framework import serializers

from apps.my_auth.models import CustomUser
from apps.my_auth.serializers import BasicCustomUserSerializer

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    team_captain = BasicCustomUserSerializer()
    teammate = BasicCustomUserSerializer()

    class Meta:
        model = Friend
        exclude = ['created', 'modified']

    def validate(self, data):
        """
        Makes sure the friends is okay
        """
        # This is making sure the two users are different
        if data['team_captain'] == data['teammate']:
            raise serializers.ValidationError("Users must be different.")

        return data

    def to_representation(self, instance):
        from apps.games.models import Game

        representation = super().to_representation(instance)
        wins = 0
        losses = 0

        for game in Game.objects.friends_games(instance):
            if game.didWin(instance):
                wins += 1
            else:
                losses += 1
        representation['wins'] = wins
        representation['losses'] = losses

        return representation


class FriendCreateSerializer(serializers.ModelSerializer):
    teammate = serializers.CharField()
    status = serializers.ChoiceField([item[0] for item in Friend.STATUS_CHOICES])

    class Meta:
        model = Friend
        fields = ['teammate', 'status']

    def validate_teammate(self, value):
        teammate = CustomUser.objects.filter(username=value)
        if not teammate.exists():
            raise serializers.ValidationError('Teammate not a user.')
        return teammate.first()

    def validate(self, data):
        """
        Makes sure the friends is okay
        """
        team_captain = self.context.get('team_captain')
        teammate = data['teammate']

        # This is making sure the two users are different
        if team_captain == teammate:
            raise serializers.ValidationError("Users must be different.")

        if not Friend.objects.friendship_exists(team_captain, teammate):
            # If the friendship doesn't exist, then the status cannot be nothing
            if data['status'] == Friend.STATUS_NOTHING:
                raise serializers.ValidationError('Cannot create a "Nothing" friend request.')
            return data

        # Since we know it exists
        friendship = Friend.objects.get_friendship(team_captain, teammate)

        # Now I have to check a lot of things.
        if friendship.status == Friend.STATUS_BLOCKED:
            if friendship.is_captain(team_captain):
                if data['status'] in [Friend.STATUS_PENDING, Friend.STATUS_ACCEPTED]:
                    raise serializers.ValidationError('This action is not allowed when blocking.')
            else:
                raise serializers.ValidationError('This action is not allowed when blocked.')
        elif friendship.status == Friend.STATUS_ACCEPTED:
            if data['status'] == Friend.STATUS_PENDING:
                estr = 'Cannot go from accepted friend request to pending.'
                raise serializers.ValidationError(estr)
        return data

    def create(self, validated_data):
        # First I will check if a friend request already exists
        team_captain = self.context.get('team_captain')
        teammate = validated_data.pop('teammate')
        status = validated_data.pop('status')

        created, friend = Friend.objects.get_or_create_friend(team_captain, teammate)

        if created:
            if status == Friend.STATUS_BLOCKED:
                friend.status = Friend.STATUS_BLOCKED
            elif status == Friend.STATUS_NOTHING:
                friend.status = Friend.STATUS_NOTHING
            elif status == Friend.STATUS_PENDING:
                friend.status = Friend.STATUS_PENDING
            elif status == Friend.STATUS_ACCEPTED:
                friend.status = Friend.STATUS_PENDING
        else:
            # This is when the team_captain is the one sending the request
            if friend.team_captain == team_captain:
                if friend.status == Friend.STATUS_BLOCKED:
                    if status == Friend.STATUS_NOTHING:
                        friend.status = Friend.STATUS_NOTHING
                elif friend.status == Friend.STATUS_NOTHING:
                    if status == Friend.STATUS_BLOCKED:
                        friend.status = Friend.STATUS_BLOCKED
                    elif status in [Friend.STATUS_PENDING, Friend.STATUS_ACCEPTED]:
                        friend.status = Friend.STATUS_PENDING
                elif friend.status == Friend.STATUS_PENDING:
                    if status == Friend.STATUS_BLOCKED:
                        friend.status = Friend.STATUS_BLOCKED
                    elif status == Friend.STATUS_NOTHING:
                        friend.status = Friend.STATUS_NOTHING
                elif friend.status == Friend.STATUS_ACCEPTED:
                    if status == Friend.STATUS_BLOCKED:
                        friend.status = Friend.STATUS_BLOCKED
                    elif status == Friend.STATUS_NOTHING:
                        friend.status = Friend.STATUS_NOTHING
            # This is when the teammate is the one sending the request
            else:
                if friend.status == Friend.STATUS_NOTHING:
                    if status == Friend.STATUS_BLOCKED:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        friend.team_captain = team_captain
                        friend.teammate = teammate
                        friend.status = Friend.STATUS_BLOCKED
                    elif status in [Friend.STATUS_PENDING, Friend.STATUS_ACCEPTED]:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        friend.team_captain = team_captain
                        friend.teammate = teammate
                        friend.status = Friend.STATUS_PENDING
                elif friend.status == Friend.STATUS_PENDING:
                    if status == Friend.STATUS_BLOCKED:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        friend.team_captain = team_captain
                        friend.teammate = teammate
                        friend.status = Friend.STATUS_BLOCKED
                    elif status == Friend.STATUS_NOTHING:
                        friend.status = Friend.STATUS_NOTHING
                    elif status == Friend.STATUS_ACCEPTED:
                        friend.status = Friend.STATUS_ACCEPTED
                elif friend.status == Friend.STATUS_ACCEPTED:
                    if status == Friend.STATUS_BLOCKED:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        friend.team_captain = team_captain
                        friend.teammate = teammate
                        friend.status = Friend.STATUS_BLOCKED
                    elif status == Friend.STATUS_NOTHING:
                        friend.status = Friend.STATUS_NOTHING

        friend.save()
        return friend

    def to_representation(self, instance):
        return FriendSerializer(instance).data
