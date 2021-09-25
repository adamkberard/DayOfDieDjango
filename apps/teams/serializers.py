from rest_framework import serializers

from apps.my_auth.models import CustomUser
from apps.my_auth.serializers import CustomUserReadSerializer

from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    team_captain = CustomUserReadSerializer()
    teammate = CustomUserReadSerializer()

    class Meta:
        model = Team
        exclude = ['created', 'modified']

    def validate(self, data):
        """
        Makes sure the teams is okay
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

        for game in Game.objects.get_team_games(instance):
            if game.didWin(instance):
                wins += 1
            else:
                losses += 1
        representation['wins'] = wins
        representation['losses'] = losses

        return representation


class TeamCreateSerializer(serializers.ModelSerializer):
    teammate = serializers.CharField()
    status = serializers.ChoiceField([item[0] for item in Team.STATUS_CHOICES])

    class Meta:
        model = Team
        fields = ['teammate', 'status']

    def validate_teammate(self, value):
        teammate = CustomUser.objects.filter(username=value, is_staff=False)
        if not teammate.exists():
            raise serializers.ValidationError('Teammate not a user.')
        return teammate.first()

    def validate(self, data):
        """
        Makes sure the teams is okay
        """
        team_captain = self.context.get('team_captain')
        teammate = data['teammate']

        # This is making sure the two users are different
        if team_captain == teammate:
            raise serializers.ValidationError("Users must be different.")

        if not Team.objects.team_exists(team_captain, teammate):
            # If the teamship doesn't exist, then the status cannot be nothing
            if data['status'] == Team.STATUS_NOTHING:
                raise serializers.ValidationError('Cannot create a "Nothing" team request.')
            return data

        # Since we know it exists
        teamship = Team.objects.get_team(team_captain, teammate)

        # Now I have to check a lot of things.
        if teamship.status == Team.STATUS_BLOCKED:
            if teamship.is_captain(team_captain):
                if data['status'] in [Team.STATUS_PENDING, Team.STATUS_ACCEPTED]:
                    raise serializers.ValidationError('This action is not allowed when blocking.')
            else:
                raise serializers.ValidationError('This action is not allowed when blocked.')
        elif teamship.status == Team.STATUS_ACCEPTED:
            if data['status'] == Team.STATUS_PENDING:
                estr = 'Cannot go from accepted team request to pending.'
                raise serializers.ValidationError(estr)
        return data

    def create(self, validated_data):
        # First I will check if a team request already exists
        team_captain = self.context.get('team_captain')
        teammate = validated_data.pop('teammate')
        status = validated_data.pop('status')

        created, team = Team.objects.get_or_create_team(team_captain, teammate)

        if created:
            if status == Team.STATUS_ACCEPTED:
                team.status = Team.STATUS_PENDING
            else:
                team.status = status
        else:
            # This is when the team_captain is the one sending the request
            if team.team_captain == team_captain:
                if team.status == Team.STATUS_BLOCKED:
                    if status == Team.STATUS_NOTHING:
                        team.status = Team.STATUS_NOTHING
                elif team.status == Team.STATUS_NOTHING:
                    if status == Team.STATUS_BLOCKED:
                        team.status = Team.STATUS_BLOCKED
                    elif status in [Team.STATUS_PENDING, Team.STATUS_ACCEPTED]:
                        team.status = Team.STATUS_PENDING
                elif team.status == Team.STATUS_PENDING:
                    if status == Team.STATUS_BLOCKED:
                        team.status = Team.STATUS_BLOCKED
                    elif status == Team.STATUS_NOTHING:
                        team.status = Team.STATUS_NOTHING
                elif team.status == Team.STATUS_ACCEPTED:
                    if status == Team.STATUS_BLOCKED:
                        team.status = Team.STATUS_BLOCKED
                    elif status == Team.STATUS_NOTHING:
                        team.status = Team.STATUS_NOTHING
            # This is when the teammate is the one sending the request
            else:
                if team.status == Team.STATUS_NOTHING:
                    if status == Team.STATUS_BLOCKED:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        team.team_captain = team_captain
                        team.teammate = teammate
                        team.status = Team.STATUS_BLOCKED
                    elif status in [Team.STATUS_PENDING, Team.STATUS_ACCEPTED]:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        team.team_captain = team_captain
                        team.teammate = teammate
                        team.status = Team.STATUS_PENDING
                elif team.status == Team.STATUS_PENDING:
                    if status == Team.STATUS_BLOCKED:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        team.team_captain = team_captain
                        team.teammate = teammate
                        team.status = Team.STATUS_BLOCKED
                    elif status == Team.STATUS_NOTHING:
                        team.status = Team.STATUS_NOTHING
                    elif status == Team.STATUS_ACCEPTED:
                        team.status = Team.STATUS_ACCEPTED
                elif team.status == Team.STATUS_ACCEPTED:
                    if status == Team.STATUS_BLOCKED:
                        # Since the requester is always the team_captain, this reverses them
                        # since we know the requester needs to become the team captain
                        team.team_captain = team_captain
                        team.teammate = teammate
                        team.status = Team.STATUS_BLOCKED
                    elif status == Team.STATUS_NOTHING:
                        team.status = Team.STATUS_NOTHING

        team.save()
        return team

    def to_representation(self, instance):
        return TeamSerializer(instance).data
