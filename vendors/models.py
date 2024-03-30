import uuid

from django.db import models
from account.models import CustomUser


class Vendor(models.Model):
    vendor_code = models.CharField(max_length=100, unique=True, editable=False, null= True)
    description = models.TextField()

    def __str__(self):
        return self.profile.name

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            self.vendor_code = 'VEN' + str(uuid.uuid4())[:5]
        super().save(*args, **kwargs)


class BusinessType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services', blank=True, null=True)

    def __str__(self):
        return self.service.name


class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product