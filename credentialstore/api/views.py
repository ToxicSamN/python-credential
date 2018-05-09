# api/views.py

from django.shortcuts import render
from rest_framework import generics
from .serializers import ClientSerializer, ClientCreateSerializer , SecretSerializer
from .models import Client, Secret


class ClientListView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreateView(generics.CreateAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer

    def perform_create(self, serializer):
        serializer.save()