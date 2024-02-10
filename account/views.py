from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import CustomUser, UserProfile
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer
)


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
        serializer = CustomUserSerializer(data= request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            
            if CustomUser.objects.filter(email = email).exists():
                return Response(
                    {'details': 'User already exists', 'code' : 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = CustomUser.objects.create_user(email = email, password = password)
            
            return Response(
                    {'detail': serializer.data, 'code': 201},
                    status=status.HTTP_201_CREATED
                )
        return Response(
            {'detail': serializer.errors, 'code' : 400},
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
    
    # def update(self, request, pk= None):
    #     try:
    #         user = CustomUser.objects.get(id = pk)
    #     except CustomUser.DoesNotExist:
    #         return Response(
    #             {'detail': 'User not found', 'code': 404},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #     serializer = CustomUserSerializer(user, data = request.data)
    #     if not serializer.is_valid():
    #         return Response(
    #             {'detail': serializer.error, 'code': 400},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
            
    #     serializer.save()
    #     return Response(
    #         {'detail' : 'Updated', 'code': 200},
    #         status=status.HTTP_200_OK
    #     )
    
    
    def update(self, request, pk = None):
        try:
            user = CustomUser.objects.get(id = pk)
        except CustomUser.DoesNotExist:
            return Response(
                {'details': 'Could not find User', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        #Allow change of email but the email should not be changed to an already existing email.  
        serializer = CustomUserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'details': 'Updated succefully', 'code':200},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'details': serializer.errors, 'code':400},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk = None):
        CustomUser.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Success', 'code': 200},
            status=status.HTTP_200_OK
        )