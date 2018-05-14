# api/serializers.py

from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from .models import Secret, Client



class SecretSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = Secret
        fields = ('username', 'password')
        read_only_fields = ('date_created', 'date_modified')


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = Client
        fields = ('pubkey', 'name')
        read_only_fields = ('date_created', 'date_modified', 'ClientId')


class ClientCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = Client
        fields = ('ClientId', 'pubkey', 'name')
        read_only_fields = ('date_created', 'date_modified')
