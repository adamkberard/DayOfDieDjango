from rest_framework import serializers

from apps.my_auth.models import CustomUser
from tools.ids_encoder import encode_id

from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        return Team.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timeRequested = validated_data.get('timeRequested',
                                                    instance.timeRequested)
        instance.timeRespondedTo = validated_data.get('timeRespondedTo',
                                                      instance.timeRespondedTo)
        instance.teamCaptain = validated_data.get('teamCaptain',
                                                instance.teamCaptain)
        instance.teammate = validated_data.get('teammate',
                                                instance.teammate)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance

    def to_representation(self, instance):
        """
        Changes the id to hashed id before it sends it out
        """
        ret = super().to_representation(instance)

        if ret['id'] is not None:
            ret['id'] = encode_id(ret['id'])

        # Changes the team id's to their usernames
        teamId = ret['teamCaptain']
        ret['teamCaptain'] = CustomUser.objects.get(id=teamId).username
        teamId = ret['teammate']
        ret['teammate'] = CustomUser.objects.get(id=teamId).username
        return ret
