from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()