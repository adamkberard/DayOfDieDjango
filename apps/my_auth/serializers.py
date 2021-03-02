from rest_framework import serializers

from .models import CustomUser


class MyAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.Serializer):
    class Meta:
        module = CustomUser

    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        return instance
