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

