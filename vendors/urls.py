from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorViewSet,
    ProductViewSet,
    OrderViewSet,
    ServicesViewSet,
    BusinessTypeViewSet,
)

router = DefaultRouter()
router.register('vendors', VendorViewSet, basename='vendor')
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')
router.register('services', ServicesViewSet, basename='services')
router.register('business_types', BusinessTypeViewSet, basename='business_types')

urlpatterns = [
    path('', include(router.urls))
    ]