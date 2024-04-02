from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Vendor, CoreServicesType, VendorService, CatalogueItem
from account.models import CustomUser
from .serializers import (
    VendorSerializer,
    CoreServiceTypeSerializer,
    VendorServiceSerializer,
    CatalogueItemSerializer
)


class VendorViewSet(viewsets.ViewSet):
    def create(self, request):
        user_id = request.data.get("user")
        try:
            CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'msg': 'User does not exist', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

        if Vendor.objects.filter(user=user_id).exists():
            return Response(
                {'msg': 'Vendor already exists', 'code': 400},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = VendorSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'msg': 'Failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': 'Successfull', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        if not serializer.data:
            return Response(
                {'msg': 'No vendors yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'msg': 'Fetched Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(id =pk)
        except Vendor.DoesNotExist:
            return Response (
                {'msg': "Could not find Vendor", 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer =VendorSerializer(vendor)

        if not serializer.data:
            return Response(
                {'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'msg': 'Fetched Successfully', 'data': serializer.data},status=status.HTTP_200_OK)

    def update(self, request, pk = None):

        try:
            vendor = Vendor.objects.get(id = pk)
        except Vendor.DoesNotExist:
            return Response(
                {'msg': 'Vendor does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = VendorSerializer(vendor, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {'msg': 'Failed', 'data': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'msg': 'Update succesful', 'code': 400},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk = None):
        Vendor.objects.get(id = pk).delete()
        return Response(
            {'msg': 'Vendor deleted', 'code': 200},
            status=status.HTTP_200_OK
        )


class CoreServicesViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CoreServiceTypeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg':'Failed', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg':'Service Created successfully', 'data': serializer.data, 'code': 200}, status=status.HTTP_201_CREATED)

    def list(self, request):
        services = CoreServicesType.objects.all()
        serializer = CoreServiceTypeSerializer(services, many=True)
        if not serializer.data:
            return Response(
                {'msg': 'No services yet', 'code': 200},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'msg':'Fetch successful', 'data': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        try:
            coreservice = CoreServicesType.objects.get(service_id=pk)
        except CoreServicesType.DoesNotExist:
            return Response(
                {'msg': 'Service does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CoreServiceTypeSerializer(coreservice)
        return Response(
            {'msg':'Fetch successful', 'data': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        try:
            coreservice = CoreServicesType.objects.get(service_id=pk)
        except CoreServicesType.DoesNotExist:
            return Response(
                {'msg': 'Service does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CoreServiceTypeSerializer(coreservice, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'msg':'Failed', 'data': serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'msg': 'Update successful', 'code': 200},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        CoreServicesType.objects.get(service_id=pk).delete()
        return Response(
            {'msg': 'Service deleted', 'code': 200},
            status=status.HTTP_200_OK
        )


class VendorServiceViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = VendorServiceSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'msg': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg':'Service added successfully', 'code': 200}, status=status.HTTP_201_CREATED)

    def list(self, request):
        services = VendorService.objects.all()
        serializer = VendorServiceSerializer(services, many=True)
        if not serializer.data:
            return Response({'msg': 'No services yet', 'code': 200}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Fetch successful', 'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            service = VendorService.objects.get(id=pk)
        except VendorService.DoesNotExist:
            return Response({'msg': 'Service does not exist', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VendorServiceSerializer(service)
        return Response({'msg':'Fetch successful', 'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            vendor_service = VendorService.objects.get(id=pk)
        except VendorService.DoesNotExist:
            return Response({'msg': 'Vendor service does not exist', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VendorServiceSerializer(
            vendor_service,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response({'msg': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': 'Update successful', 'code': 200}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        VendorService.objects.get(id=pk).delete()
        return Response({'msg': 'Vendor service deleted', 'code': 200}, status=status.HTTP_200_OK)


class CatalogueItemViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = CatalogueItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': 'Catalogue itm added successfully', 'code': 200}, status=status.HTTP_201_CREATED)

    def list(self, request):
        items = CatalogueItem.objects.all()
        serializer = CatalogueItemSerializer(items, many=True)
        if not serializer.data:
            return Response({'msg': 'No items yet', 'code': 200}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Fetch successful', 'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            item = CatalogueItem.objects.get(id=pk)
        except CatalogueItem.DoesNotExist:
            return Response({'msg': 'Item does not exist', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CatalogueItemSerializer(item)
        return Response({'msg': 'Fetch successful', 'data': serializer.data, 'code': 200}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            item = CatalogueItem.objects.get(id=pk)
        except CatalogueItem.DoesNotExist:
            return Response({'msg': 'Item does not exist', 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CatalogueItemSerializer(item, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'msg': serializer.errors, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msd': 'Update successful', 'code': 200}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        CatalogueItem.objects.get(id=pk).delete()
        return Response({'msg': 'Item deleted', 'code': 200}, status=status.HTTP_200_OK)
