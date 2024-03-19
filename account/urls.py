from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    UserProfileViewSet,
    LoginViewSet,
    LogoutViewSet
)

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'profiles', UserProfileViewSet, basename='users')
router.register(r'login', LoginViewSet, basename='users')
router.register(r'logout', LogoutViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
