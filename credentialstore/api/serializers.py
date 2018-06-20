# api/serializers.py

from rest_framework import serializers
from .models import SecretModel, ClientModel, AdminModel


class SecretListSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = SecretModel
        fields = ('Username', 'Password')
        read_only_fields = ('date_created', 'date_modified')


class ClientListSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    secret = SecretListSerializer(read_only=True, many=True)

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = ClientModel
        fields = ('ClientId', 'pubkey', 'secret')
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


class AdminSecretSerializer(serializers.ModelSerializer):
    """
        Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = SecretModel
        fields = ('Username', 'Password', 'date_created', 'date_modified')
        read_only_fields = ()


class AdminClientSerializer(serializers.ModelSerializer):
    """
        Serializer to map the Model instance into JSON format.
    """

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = ClientModel
        fields = ('ClientId', 'pubkey', 'name', 'date_created', 'date_modified')


class AdminClientListSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """

    secret = AdminSecretSerializer(read_only=True, many=True)

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = ClientModel
        fields = ('ClientId', 'pubkey', 'secret')
        read_only_fields = ('date_created', 'date_modified', 'ClientId')


class AdminSecretClientListSerializer(serializers.ModelSerializer):

    clients = AdminClientSerializer(read_only=True, many=True)

    class Meta:
        """
        Map this serializer to a model and their fields.
        """
        model = SecretModel
        fields = ('Username', 'clients', 'date_created', 'date_modified')


# class AdminList(serializers.ModelSerializer):
#
#     class Meta:
#         """
#         Map this serializer to a model and their fields.
#         """
#         model = AdminModel
#         fields = ('AdminId', 'date_created', 'date_modified')