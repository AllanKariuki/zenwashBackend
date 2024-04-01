from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorViewSet,
    CoreServicesViewSet,
    VendorServiceViewSet,
    CatalogueItemViewSet
)

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'service-types', CoreServicesViewSet, basename='service')
router.register(r'vendor-services', VendorServiceViewSet, basename='vendor-service')
router.register(r'catalogue-items', CatalogueItemViewSet, basename='catalogue-item')

urlpatterns = [
    path('', include(router.urls))
    ]