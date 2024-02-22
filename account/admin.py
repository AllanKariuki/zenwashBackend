from django.contrib import admin

from .models import CustomUser
from .models import UserProfile

admin.site.register(CustomUser)
admin.site.register(UserProfile)
