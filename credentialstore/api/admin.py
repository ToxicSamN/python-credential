# /api/admin.py

from django.contrib import admin
#from credentialstore.credentialstore.admin import CustomAdminSite
from .models import SecretModel, ClientModel, AdminModel


class SecretAdminModel(admin.ModelAdmin):
    list_display = ('username',)


class ClientAdminModel(admin.ModelAdmin):
    list_display = ('ClientId', 'name',)


# Register your models here.
admin.site.register(SecretModel, SecretAdminModel)
admin.site.register(ClientModel, ClientAdminModel)
admin.site.register(AdminModel)
