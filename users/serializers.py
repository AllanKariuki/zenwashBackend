from rest_framework import serializers

from .models import Order, OrderItem
from account.serializers import CustomUserSerializer
from vendors.serializers import VendorServiceSerializer, VendorSerializer, CatalogueItemSerializer
from vendors.models import VendorService, CatalogueItem, Vendors


class OrderItemSerializer(serializers.ModelSerializer):
    service=VendorServiceSerializer(required=False)
    vendor=VendorSerializer(required=False)
    item=CatalogueItemSerializer(required=True)

    class Meta:
        model=OrderItem
        fields="__all__"

    def validate(self, data):
        service_id = self.context['request'].get('service')
        vendor_id = self.context['request'].get('vendor')
        item_id = self.context['request'].get('item')
        try:
            self.service = VendorService.objects.get(service=service_id)
        except VendorService.DoesNotExist:
            raise serializers.ValidationError('Service Does not exist')
        try:
            self.vendor = Vendors.objects.get(id=vendor_id)
        except Vendors.DoesNotExist:
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
    user = CustomUserSerializer(require=False)
    item = serializers.SerializerMethodField('get_order_items')

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        order_item = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_item, many=True)
        return serializer.data


