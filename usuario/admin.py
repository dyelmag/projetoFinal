from django.contrib import admin
from .models import Perfil
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.

admin.site.register(Perfil)
TokenAdmin.raw_id_fields = ('user',)