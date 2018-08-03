#  api/forms.py

from django import forms
from django.db import models
from .models import SecretModel


class SecretModelForm(forms.ModelForm):

    class Meta:
        model = SecretModel
        fields = ['username', 'password']
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }

    # show_password = forms.CheckboxInput


