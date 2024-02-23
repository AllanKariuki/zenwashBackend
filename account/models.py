from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import CASCADE
from PIL import Image

from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("Email address"), unique = True)
    password = models.CharField(max_length= 100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = CASCADE)
    name = models.CharField(max_length= 100)
    phone_number = models.IntegerField()
    location = models.CharField(max_length= 200)
    image_url = models.ImageField(upload_to = 'profile_pics', default = 'default.jpg', blank = True, null = True)
    
    def __str__(self):
        return self.name