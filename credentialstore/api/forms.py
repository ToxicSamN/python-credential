#  api/forms.py

from django import forms
from django.db import models
from .models import SecretModel


class SecretModelForm(forms.ModelForm):

    show_password = forms.PasswordInput()

    class Meta:
        model = SecretModel
        fields = ['username', 'password', 'show_password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class SecretWithCheckBoxForm(SecretModelForm):

    class Meta(SecretModelForm.Meta):

        fields = SecretModelForm.Meta.fields
        fields.append('show_password',)


class PasswordField(forms.CharField):
    widget = forms.PasswordInput


class PasswordModelField(models.CharField):
    """
    This class is to create a new model form field type for passwords
    This isn't built in to the model forms by default
    """
    def formfield(self, **kwargs):
        defaults = {'form_class': PasswordField}
        defaults.update(kwargs)
        return super(PasswordModelField, self).formfield(**defaults)
