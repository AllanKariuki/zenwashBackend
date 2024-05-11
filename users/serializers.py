from rest_framework import serializers

from .models import Order, OrderItem
from account.serializers import CustomUserSerializer
from vendors.serializers import VendorServiceSerializer, VendorSerializer, CatalogueItemSerializer
from vendors.models import VendorService, CatalogueItem, Vendor


class OrderItemSerializer(serializers.ModelSerializer):
    service=VendorServiceSerializer(read_only=True)
    vendor=VendorSerializer(read_only=True)
    item=CatalogueItemSerializer(read_only=True)
    service_id=serializers.CharField(write_only=True)
    vendor_id=serializers.IntegerField(write_only=True)
    item_id=serializers.IntegerField(write_only=True)

    class Meta:
        model=OrderItem
        fields="__all__"

    def validate(self, data):
        service_id = data.get('service_id')
        vendor_id = data.get('vendor_id')
        item_id = data.get('item_id')

        if service_id is None:
            raise serializers.ValidationError({"service_id": "This field is required."})
        if vendor_id is None:
            raise serializers.ValidationError({"vendor_id": "This field is required."})
        if item_id is None:
            raise serializers.ValidationError({"item_id": "This field is required."})
        try:
            self.service = VendorService.objects.get(id=service_id)
        except VendorService.DoesNotExist:
            raise serializers.ValidationError('Service Does not exist')
        try:
            self.vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            raise serializers.ValidationError('Vendor Does not exist')
        try:
            self.item = CatalogueItem.objects.get(id=item_id)
        except CatalogueItem.DoesNotExist:
            raise serializers.ValidationError('Item Does not exist')
        return data

    def create(self, validated_data):
        order_item = OrderItem.objects.create(service=self.service, vendor=self.vendor, item=self.item, **validated_data)
        return order_item

    def update(self, instance, validated_data):
        instance.service=self.service
        instance.vendor=self.vendor
        instance.item=self.item
        instance.quantity=validated_data.get('quantity', instance.quantity)
        instance.amount=validated_data.get('amount', instance.amount)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    # user = CustomUserSerializer(read_only=False)
    item = serializers.SerializerMethodField('get_order_items')

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        order_item = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_item, many=True)
        return serializer.data


