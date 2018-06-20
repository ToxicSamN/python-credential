from django.contrib import admin
from .models import SecretModel, ClientModel, AdminModel

# Register your models here.
admin.site.register(SecretModel)
admin.site.register(ClientModel)
admin.site.register(AdminModel)