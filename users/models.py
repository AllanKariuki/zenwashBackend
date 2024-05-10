from django.db import models

from account.models import CustomUser
from vendors.models import VendorService, Vendor, CatalogueItem

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(VendorService, on_delete=models.CASCADE)
    item = models.ForeignKey(CatalogueItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item.item_name