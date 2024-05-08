from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ServicesListingViewset

router = DefaultRouter()

router.register(r"services", ServicesListingViewset, basename="services")

urlpatterns = [
    path("", include(router.urls))
]