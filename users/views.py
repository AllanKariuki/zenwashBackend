from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from vendors.models import Vendor, CoreServicesType, VendorService, CatalogueItem, Reviews
from vendors.serializers import VendorSerializer, CoreServiceTypeSerializer, VendorServiceSerializer, CatalogueItemSerializer
from .utils import get_nearby_services
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class ServicesListingViewset(viewsets.ViewSet):

    def list(self, request):
        pass


    def retrieve(self, request, pk=None):
        user = request.user
        print(user)
        try:
            coreservice = CoreServicesType.objects.get(service_id=pk)
            vendor_services = VendorService.objects.filter(service=coreservice)
        except CoreServicesType.DoesNotExist:
            return Response(
                {'msg': 'Service does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        services_list = get_nearby_services(coreservice, 54.0, 38.0)
        serializer = VendorServiceSerializer(services_list, many=True)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

class OrderViewset(viewsets.ViewSet):

    def list(self, request):
        pass

    def create(self, request):
        # Create an order
        order_data = {
            "user": request.data.get('user'),
            "total_amount": request.data.get('total_amount')
        }
        order_serializer = OrderSerializer(data=order_data)
        if not order_serializer.is_valid():
            return Response({'msg': order_serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        order=order_serializer.save()
        items = request.data.get('items', [])
        for item in items:
            item['order'] = order.id
            order_item_serializer = OrderItemSerializer(data=item, context={'request': request})
            if not order_item_serializer.is_valid():
                return Response({'msg': order_item_serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
            order_item_serializer.save()
        return Response({'msg': 'Order created successfully', 'code': 201}, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass