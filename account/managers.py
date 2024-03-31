from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError(_("Email missing"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        password = extra_fields.pop("password")
        if password:
            user.password = make_password(password)
        else:
            raise ValueError(_("Password missing"))
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        user = self.create_user(email, password, **extra_fields)
        # CustomToken.objects.create(user=user)
              
        # return self.create_user(email, password, **extra_fields)
        return user