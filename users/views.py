from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from vendors.models import Vendor, CoreServicesType, VendorService, CatalogueItem, Reviews
from vendors.serializers import VendorSerializer, CoreServiceTypeSerializer, VendorServiceSerializer, CatalogueItemSerializer
from .utils import get_nearby_services

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
