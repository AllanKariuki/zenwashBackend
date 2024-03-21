from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import CASCADE
from PIL import Image
import os
import binascii

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
    image_url = models.ImageField(upload_to='profile_pics', default='default.jpg', blank=True, null=True)
    
    def __str__(self):
        return self.name


class CustomToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        CustomUser, related_name='authentication_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("CustomToken")
        verbose_name_plural = _("CustomTokens")

    def save(self, *args, **kwargs):
        self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f"{self.key} - ({self.user.email})"


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")
