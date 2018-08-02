# /api/admin.py

from django.contrib import admin
from .models import SecretModel, ClientModel


class SecretAdminModel(admin.ModelAdmin):
    list_display = ('username',)


class ClientAdminModel(admin.ModelAdmin):
    list_display = ('ClientId', 'name',)


# Register your models here.
admin.site.register(SecretModel, SecretAdminModel)
admin.site.register(ClientModel, ClientAdminModel)
