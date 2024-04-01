from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, UserLoginViewSet, LogoutViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls))
]
