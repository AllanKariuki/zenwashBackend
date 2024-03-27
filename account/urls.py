from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, UserProfileViewSet, UserLoginViewSet, LogoutViewSet

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'profiles', UserProfileViewSet, basename='profiles')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls))
]
