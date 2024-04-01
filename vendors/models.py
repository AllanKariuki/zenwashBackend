import uuid

from django.db import models
from account.models import CustomUser


class Vendor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vendor_code = models.CharField(max_length=100, unique=True, editable=False, null= True)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            self.vendor_code = 'VEN' + str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)


class CoreServicesType(models.Model):
    service_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_name = models.CharField(max_length=100)
    service_image = models.ImageField(upload_to='service_types', default='default_service.jpg', blank=True, null=True)

    def __str__(self):
        return self.service_name


class VendorService(models.Model):
    service = models.ForeignKey(CoreServicesType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    motto = models.TextField()
    service_image = models.ImageField(upload_to='vendor_services', default='default_service.png', blank=True, null=True)

    def __str__(self):
        return self.name


class CatalogueItem(models.Model):
    vendor_service = models.ForeignKey(VendorService, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_image = models.ImageField(upload_to='catalogue_items', default='default_item.jpg', blank=True, null=True)

    def __str__(self):
        return self.item_name


class Reviews(models.Model):
    vendor_service = models.ForeignKey(VendorService, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
