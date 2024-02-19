from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register('vendor', VendorViewSet)
router.register('product', ProductViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
    ]