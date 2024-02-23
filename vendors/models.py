from django.db import models
from account.models import CustomUser, UserProfile

class Vendor(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.profile.name

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