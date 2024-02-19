from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, Product, Order
from .serializers import VendorSerializer, ProductSerializer, OrderSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()

    def create(self, request):
        serializer = VendorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def list(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        if not serializer.data:
            return Response(
                {'detail': 'No vendors yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def update(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def destroy(self, instance):
        instance.delete()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.profile.vendor)

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.profile.vendor)

    def perform_update(self, serializer):
        serializer.save(vendor=self.request.user.profile.vendor)

    def perform_destroy(self, instance):
        instance.delete()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()