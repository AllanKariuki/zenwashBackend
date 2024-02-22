from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register('vendors', VendorViewSet, basename='vendor')
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls))
    ]