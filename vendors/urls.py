from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorViewSet,
    ProductViewSet,
    OrderViewSet,
    ServicesViewSet,
    BusinessTypeViewSet,
    ServiceImageViewSet
)

router = DefaultRouter()
router.register('vendors', VendorViewSet, basename='vendor')
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')
router.register('services', ServicesViewSet, basename='services')
router.register('business_types', BusinessTypeViewSet, basename='business_types')
router.register('service_images', ServiceImageViewSet, basename='service_images')

urlpatterns = [
    path('', include(router.urls))
    ]