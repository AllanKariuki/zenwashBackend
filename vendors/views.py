from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Vendor, Product, Order, BusinessType, Services, ServiceImage
from account.models import CustomUser
from .serializers import (
    VendorSerializer,
    ProductSerializer,
    OrderSerializer,
    BusinessTypeSerializer,
    ServicesSerializer,
    ServiceImageSerializer,
)


class BusinessTypeViewSet(viewsets.ViewSet):
    def list(self, request):
        business_types = BusinessType.objects.all()
        serializer = BusinessTypeSerializer(business_types, many=True)
        if not serializer.data:
            return Response(
                {'detail': 'No business types yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )
    def retrieve(self, request, pk=None):
        try:
            business_type = BusinessType.objects.get(id = pk)
        except BusinessType.DoesNotExist:
            return Response (
                {'detail': "Could not find Business Type", 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer =BusinessTypeSerializer(business_type)

        if not serializer.data:
            return Response(
                {'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )
    def create(self, request):
        serializer = BusinessTypeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk = None):
        try:
            business_type = BusinessType.objects.get(id = pk)
        except BusinessType.DoesNotExist:
            return Response(
                {'detail': 'Business Type does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = BusinessTypeSerializer(business_type, data= request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'detail': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'detail': 'Update succesful', 'code': 400},
            status=status.HTTP_200_OK
        )
    def destroy(self, request, pk = None):
        BusinessType.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Business Type deleted', 'code': 200},
            status=status.HTTP_200_OK
        )

class ServicesViewSet(viewsets.ViewSet):
    def list(self, request):
        services = Services.objects.all()
        serializer = ServicesSerializer(services, many=True)
        if not serializer.data:
            return Response(
                {'detail': 'No services yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        try:
            service = Services.objects.get(id = pk)
        except Services.DoesNotExist:
            return Response (
                {'detail': "Could not find Service", 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer =ServicesSerializer(service)

        if not serializer.data:
            return Response(
                {'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def create(self, request):
        buss_type_id = request.data.get("business_type")
        vendor_id = request.data.get("vendor")

        try:
            business_type = BusinessType.objects.get(id = buss_type_id)
        except BusinessType.DoesNotExist:
            return Response(
                {'detail': 'Business Type does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        if not Vendor.objects.filter(id = vendor_id).exists():
            return Response(
                {'detail': 'Vendor does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServicesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk = None):
        try:
            service = Services.objects.get(id = pk)
        except Services.DoesNotExist:
            return Response(
                {'detail': 'Service does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = ServicesSerializer(service, data= request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'detail': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'detail': 'Update succesful', 'code': 400},
            status=status.HTTP_200_OK
        )
    def destroy(self, request, pk = None):
        Services.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Service deleted', 'code': 200},
            status=status.HTTP_200_OK
        )


class VendorViewSet(viewsets.ViewSet):
    def create(self, request):

        profile_id = request.data.get("profile")

        if Vendor.objects.filter(profile = profile_id).exists():
            return Response(
                {'detail': 'Vendor already exists', 'code': 400},
                status = status.HTTP_400_BAD_REQUEST
            )
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
    def retrieve(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(id = pk)
        except Vendor.DoesNotExist:
            return Response (
                {'detail': "Could not find Vendor", 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer =VendorSerializer(vendor)

        if not serializer.data:
            return Response(
                {'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )
    def update(self, request, pk = None):
        profile_id = request.data.get("profile")
        try:
            vendor = Vendor.objects.get(id = pk)
        except UserProfile.DoesNotExist:
            return Response(
                {'detail': 'Vendor does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = VendorSerializer(vendor, data= request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'detail': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'detail': 'Update succesful', 'code': 400},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk = None):
        Vendor.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Vendor deleted', 'code': 200},
            status=status.HTTP_200_OK
        )


class ServiceImageViewSet(viewsets.ViewSet):
    def create(self, request):
        service_id = request.data.get("service")
        if not Services.objects.filter(id = service_id).exists():
            return Response(
                {'detail': 'Service does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ServiceImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        service_images = ServiceImage.objects.all()
        serializer = ServiceImageSerializer(service_images, many=True)
        if not serializer.data:
            return Response(
                {'detail': 'No service images yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        try:
            service_image = ServiceImage.objects.get(id = pk)
        except ServiceImage.DoesNotExist:
            return Response (
                {'detail': "Could not find Service Image", 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer =ServiceImageSerializer(service_image)
        if not serializer.data:
            return Response(
                {'detail': serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def update(self, request, pk = None):
        try:
            service_image = ServiceImage.objects.get(id = pk)
        except ServiceImage.DoesNotExist:
            return Response(
                {'detail': 'Service Image does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = ServiceImageSerializer(service_image, data= request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'detail': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'detail': 'Update succesful', 'code': 400},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk = None):
        ServiceImage.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Service Image deleted', 'code': 200},
            status=status.HTTP_200_OK
        )

class ProductViewSet(viewsets.ViewSet):
    """"
        Args:
            Product viewset that is responsible for creating, listing, retrieving, updating and deleting products.
            viewsets: viewsets object
        Returns:
            None
    """
    queryset = Product.objects.all()

    def create(self, request):
        """"
            Args:
                request: request object
            Returns:
                None
        """
        vendor_id = request.data.get("vendor")
        if not Vendor.objects.filter(id = vendor_id).exists():
            return Response(
                {'detail': 'Vendor does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):

        """
            Args:
                request: request object
            Returns:
                None
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        if not serializer.data:
            return Response(
                {'detail': 'No products yet'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk = None):

        """"
            Args:
                request: request object
                pk: id of the product to be retrieved
            Returns:
                None
        """

        try:
            product = Product.objects.get(id = pk)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Product does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = ProductSerializer(product)

        if not serializer.data:
            return Response(
                {'detail': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': serializer.data},
            status=status.HTTP_200_OK
        )

    def update(self, request, pk = None):
        """
            Args:
                request: request object
                pk: id of the product to be updated
            Returns:
                None
        """
        try:
            product = Product.objects.get(id = pk)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Product does not Exist', 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer = ProductSerializer(product, data= request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'detail': serializer.errors, 'code': 400},
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'detail': 'Update succesful', 'code': 400},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk = None):
        """"
            Args:
                pk: id of the product to be deleted
            Returns:
                None
        """
        Product.objects.get(id = pk).delete()
        return Response(
            {'detail': 'Product deleted', 'code': 200},
            status=status.HTTP_200_OK
        )

class OrderViewSet(viewsets.ViewSet):
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

