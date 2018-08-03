#  api/forms.py

from django import forms
from .models import SecretModel


class SecretModelForm(forms.ModelForm):

    class Meta:
        model = SecretModel
        fields = ['username', 'password']
