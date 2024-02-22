from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, Product, Order
from account.models import CustomUser, UserProfile
from .serializers import VendorSerializer, ProductSerializer, OrderSerializer


class VendorViewSet(viewsets.ModelViewSet):
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

    def destroy(self, pk = None):
        Vendor.objects.get(id = pk).delete()

class ProductViewSet(viewsets.ModelViewSet):
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

    def perform_destroy(self, pk = None):
        """"
            Args:
                pk: id of the product to be deleted
            Returns:
                None
        """
        Product.objects.get(id = pk).delete()

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