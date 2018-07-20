# /api/admin.py

from django.contrib import admin
#from credentialstore.credentialstore.admin import CustomAdminSite
from .models import SecretModel, ClientModel, AdminModel

# Register your models here.
admin.site.register(SecretModel)
admin.site.register(ClientModel)
admin.site.register(AdminModel)
