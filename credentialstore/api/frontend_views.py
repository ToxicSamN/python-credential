# api/frontend_views.py

import os
from functools import reduce
from django.core import exceptions
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ClientListSerializer, SecretListSerializer, ClientCreateSerializer
from .serializers import AdminClientListSerializer, AdminSecretClientListSerializer, AdminSecretSerializer
from .models import ClientModel, SecretModel
from.decorators import admin_login_required, create_login_required, update_login_required
from .render import CredStoreBrowsableAPIRenderer

@method_decorator(create_login_required, name='dispatch')
class CreateClientView(generics.CreateAPIView):

    queryset = ClientModel.objects.all()
    serializer_class = ClientCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


@method_decorator(update_login_required, name='dispatch')
class UpdateClientView(generics.UpdateAPIView):

    queryset = ClientModel.objects.all()
    serializer_class = ClientCreateSerializer
    renderer_classes = [CredStoreBrowsableAPIRenderer]
