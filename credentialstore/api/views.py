# api/views.py

from django.shortcuts import render
from rest_framework import generics
from .serializers import ClientSerializer, SecretSerializer
from .models import Client, Secret

class ClientCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()