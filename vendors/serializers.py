from rest_framework import serializers
from .models import Vendor
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
