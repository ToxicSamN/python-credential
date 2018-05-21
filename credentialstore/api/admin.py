from django.contrib import admin
from .models import SecretModel, ClientModel

# Register your models here.
admin.site.register(SecretModel)
admin.site.register(ClientModel)