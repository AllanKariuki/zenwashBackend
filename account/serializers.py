from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required = False)
    email = serializers.EmailField(required = True)
    name = serializers.CharField(required = True)
    phone_number = serializers.CharField(required = True)
    national_id = serializers.IntegerField(required = True)
    user_type = serializers.CharField(required = True)
    location_lat = serializers.CharField(required = True)
    location_lon = serializers.CharField(required = True)
    address = serializers.CharField(required = True)
    bio = serializers.CharField(required = True)
    image_url = serializers.ImageField(required = False)
    created_at = serializers.DateTimeField(required = False)
    updated_at = serializers.DateTimeField(required = False)
    password = serializers.CharField(required = True)

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()