# /api/admin.py

from django.contrib import admin
from .models import SecretModel, ClientModel
from .forms import SecretModelForm
from .pystuffing.secret import Secret


class SecretAdminModel(admin.ModelAdmin):
    form = SecretModelForm
    change_form_template = 'admin/change_secret_form.html'
    add_form_template = 'admin/change_secret_form.html'
    list_display = ('username',)

    def save_model(self, request, obj, form, change):
        """
        Method override so that the password that is supplied by the user is encrypted before saving to db
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        if obj.pk:
            model_obj = self.model.objects.get(pk=obj.pk)
            if not model_obj.password == obj.password:
                # password changed and we need to now encrypt the password
                obj = self.decoder_ring(obj)
        else:
            obj = self.decoder_ring(obj)

        obj.save()

    @staticmethod
    def decoder_ring(obj):
        decoder_ring = Secret()
        decoder_ring.encrypt(privateData=obj.password)
        obj.password = decoder_ring.get_encrypted_message().decode('utf-8')
        return obj

class ClientAdminModel(admin.ModelAdmin):
    list_display = ('ClientId', 'name',)


# Register your models here.
admin.site.register(SecretModel, SecretAdminModel)
admin.site.register(ClientModel, ClientAdminModel)
