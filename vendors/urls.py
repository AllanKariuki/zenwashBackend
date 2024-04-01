from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VendorViewSet,
    CoreServicesViewSet
)

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'service-types', CoreServicesViewSet, basename='service')
urlpatterns = [
    path('', include(router.urls))
    ]