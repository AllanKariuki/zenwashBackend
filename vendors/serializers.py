from rest_framework import serializers
from .models import Vendor
from account.models import CustomUser


class VendorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Vendor
        fields = '__all__'
        read_only_fields = ['vendor_code']
