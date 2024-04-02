import secrets

import bcrypt
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import CustomUser, CustomToken
from .serializers import (
    CustomUserSerializer,
    LoginSerializer
)
from .authentication import expired_token_handler, expires_in


class CustomUserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many = True)
        if not serializer.data:
            return Response(
                {'detail': 'No users yet', 'code': 200},
                status= status.HTTP_200_OK
            )
        
        return Response(
                {'detail': serializer.data, 'code': 200},
                status= status.HTTP_200_OK
            )
    
    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if CustomUser.objects.filter(email=validated_data["email"]).exists():
                return Response(
                    {'details': 'User already exists', 'code' : 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = CustomUser.objects.create_user(**validated_data)
            
            return Response(
                    {'detail': 'User Created successfully', 'code': 201},
                    status=status.HTTP_201_CREATED
                )
        return Response(
            {'detail': 'Failed', 'code' : 400},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def retrieve(self, request, pk=None):
        try:
            
            user = CustomUser.objects.get(id = pk)
        except CustomUser.DoesNotExist:
            return Response(
                {'detail': 'User not found', 'code': 404},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CustomUserSerializer(user)
        return Response(
            {'details': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
            )

    def update(self, request, pk=None):
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response(
                {'details': 'Could not find User', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CustomUserSerializer(user, data=request.data, partial=True)  # Set partial=False for full updates
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'details': 'Updated successfully', 'code': 200},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'details': serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk=None):
        CustomUser.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Success', 'code': 200},
            status=status.HTTP_200_OK
        )



class UserLoginViewSet(viewsets.ViewSet):
    def token_generator(self, user):
        """function to generate a bcrypted token"""
        key = bcrypt.hashpw(secrets.token_hex(50).encode('utf-8'), bcrypt.gensalt())
        key = key.decode('utf-8')
        token, _ = CustomToken.objects.update_or_create(user=user, defaults={'key': key})
        return token

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'details': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'details': 'Invalid credentials', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = CustomToken.objects.get(user=user)
            is_expired, token = expired_token_handler(token)
            if is_expired:
                token = self.token_generator(user)

        except CustomToken.DoesNotExist:
            token = self.token_generator(user)

        authenticated_user = CustomUserSerializer(user)
        return Response(
            {
                'success': 'Login successful',
                'user': authenticated_user.data,
                'token': token.key,
                'expires in': expires_in(token),
            },
            status=status.HTTP_200_OK
        )


class LogoutViewSet(viewsets.ViewSet):
    def create(self, request):
        request.user.authentication_token.delete()
        return Response({'detail': 'Logout successful', 'code': 200}, status=status.HTTP_200_OK)
