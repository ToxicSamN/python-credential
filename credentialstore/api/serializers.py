# api/serializers.py

from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from .models import SecretModel, ClientModel



class SecretListSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = SecretModel
        fields = ('username', 'ClientId')
        read_only_fields = ('password', 'date_created', 'date_modified')


class SecretCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = SecretModel
        fields = ('username', 'password')
        read_only_fields = ('date_created', 'date_modified')


class ClientListSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = ClientModel
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
        model = ClientModel
        fields = ('ClientId', 'pubkey', 'name')
        read_only_fields = ('date_created', 'date_modified')
