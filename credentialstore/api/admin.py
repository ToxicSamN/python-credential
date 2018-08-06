# /api/admin.py

from django.contrib import admin
from .models import SecretModel, ClientModel
from .pystuffing.secret import Secret


class SecretAdminModel(admin.ModelAdmin):
    """
    Custom ModelAdmin for the secrets model.
    This is so it can use a customized template and custom change_list table
    """
    # form = SecretModelForm
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

        # check for a primary key (pk) in the submitted obj. if the pk exists then this is an existing model obj
        #  otherwise it is a new obj to be added to the model.
        if obj.pk:
            # existing model obj
            # get the actual model_obj based ont he submitted primary key (pk)
            model_obj = self.model.objects.get(pk=obj.pk)
            if not model_obj.password == obj.password:
                # password changed and we need to now encrypt the password
                obj = self.decoder_ring(obj)
        else:
            # new obj being added to the model
            # send the password to be encrypted
            obj = self.decoder_ring(obj)

        obj.save()

    @staticmethod
    def decoder_ring(obj):
        """
        Static method for encrypting the password and savingt he encrypted value
        to the obj.password field prior to sending it to the database.
        This ensures the database has an encrypted copy of the password instead of
        clear text or a one-way hash value
        :param obj:
        :return: obj
        """
        decoder_ring = Secret()
        decoder_ring.encrypt(privateData=obj.password)
        obj.password = decoder_ring.get_encrypted_message().decode('utf-8')
        return obj


class ClientAdminModel(admin.ModelAdmin):
    """
        Custom ModelAdmin for the client model.
        This is so it can use a customized change_list table
    """
    list_display = ('ClientId', 'name',)


# Register your models here.
admin.site.register(SecretModel, SecretAdminModel)
admin.site.register(ClientModel, ClientAdminModel)
