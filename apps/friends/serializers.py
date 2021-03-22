from rest_framework import serializers

from apps.my_auth.models import CustomUser
from tools.ids_encoder import encode_id

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Friend
        fields = '__all__'

    def create(self, validated_data):
        return Friend.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timeRequested = validated_data.get('timeRequested',
                                                    instance.timeRequested)
        instance.timeRespondedTo = validated_data.get('timeRespondedTo',
                                                      instance.timeRespondedTo)
        instance.requester = validated_data.get('requester',
                                                instance.requester)
        instance.requested = validated_data.get('requested',
                                                instance.requested)
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

        # Changes the friend id's to their usernames
        friendId = ret['requester']
        ret['requester'] = CustomUser.objects.get(id=friendId).username
        friendId = ret['requested']
        ret['requested'] = CustomUser.objects.get(id=friendId).username
        return ret
