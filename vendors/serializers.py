from rest_framework import serializers
from .models import Vendor, CoreServicesType, VendorService, CatalogueItem
from account.models import CustomUser
from account.serializers import CustomUserSerializer


class VendorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['vendor_code']

    def create(self, validated_data):
        user_id = self.context['request'].data.get('user')
        user = CustomUser.objects.get(id=user_id)
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor

    def update(self, instance, validated_data):
        user_id = self.context['request'].data.get('user')
        user = CustomUser.objects.get(id=user_id)
        instance.user = user
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        instance.save()
        return instance


class CoreServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreServicesType
        fields = '__all__'


class VendorServiceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    service = CoreServiceTypeSerializer(read_only=True)

    class Meta:
        model = VendorService
        fields = '__all__'

    def create(self, validated_data):
        vendor_id = self.context['request'].data.get('vendor')
        service_id = self.context['request'].data.get('service')
        vendor = Vendor.objects.get(id=vendor_id)
        service = CoreServicesType.objects.get(service_id=service_id)
        vendor_service = VendorService.objects.create(vendor=vendor, service=service, **validated_data)
        return vendor_service

    def update(self, instance, validated_data):
        vendor_id = self.context['request'].data.get('vendor')
        vendor = Vendor.objects.get(id=vendor_id)
        service_id = self.context['request'].data.get('service')
        service = CoreServicesType.objects.get(service_id=service_id)
        instance.vendor = vendor
        instance.service = service
        instance.name = validated_data.get('name', instance.name)
        instance.motto = validated_data.get('motto', instance.motto)
        instance.service_image = validated_data.get('service_image', instance.service_image)
        instance.save()
        return instance


class CatalogueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogueItem
        fields = '__all__'
