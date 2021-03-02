from rest_framework import serializers

from tools.ids_encoder.converters import HashidsConverter

from .models import Litter


class LitterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Litter
        exclude = ['user']

    def create(self, validated_data):
        return Litter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.typeOfLitter = validated_data.get('typeOfLitter',
                                                   instance.typeOfLitter)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.timeCollected = validated_data.get('timeCollected',
                                                    instance.timeCollected)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Changes the id to hashed id before it sends it out
        """
        ret = super().to_representation(instance)
        converter = HashidsConverter()
        if ret['id'] is not None:
            ret['id'] = converter.to_url(ret['id'])
        return ret
