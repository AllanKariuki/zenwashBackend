from rest_framework import serializers
from .models import CustomUser, UserProfile

class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)
    
class UserProfileSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    name = serializers.CharField(max_length= 100)
    phone_number = serializers.IntegerField()
    location = serializers.CharField(max_length= 200)