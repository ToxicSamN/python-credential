# api/views.py

from django.shortcuts import render
from rest_framework import generics
from .serializers import ClientListSerializer, ClientCreateSerializer, SecretListSerializer, SecretCreateSerializer
from .models import ClientModel, SecretModel
from .pystuffing.secret import Secret
from .pystuffing.client import Client


class ClientListView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = ClientModel.objects.all()
    serializer_class = ClientListSerializer


class ClientCreateView(generics.CreateAPIView):

    queryset = ClientModel.objects.all()
    serializer_class = ClientCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


class SecretListView(generics.CreateAPIView):
    """
        This class will take handle what appears to be a GET request for credentials.
        It really is a POST request asking for the credentials but sending the clientID
        to the API and then it uses thi information to return the Credentials back
        in an encrypted message.
    """
    queryset = SecretModel.objects.all()
    serializer_class = SecretListSerializer

    def create(self, request, *args, **kwargs):
        print('doing something')


class SecretCreateCreateView(generics.CreateAPIView):

    queryset = SecretModel.objects.all()
    serializer_class = SecretCreateSerializer

    def perform_create(self, serializer):
        serializer.save()
