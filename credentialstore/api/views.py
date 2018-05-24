# api/views.py

import os
from functools import reduce
from django.shortcuts import render
from django.core import serializers, exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ClientListSerializer, SecretListSerializer, ClientCreateSerializer, AdminSecretClientListSerializer
from .models import ClientModel, SecretModel, AdminModel
from .pystuffing.secret import Secret
from .pystuffing.client import Client


class ModelFieldError(exceptions.FieldError):
    pass


class GetCredentialView(generics.ListAPIView):

    serializer_class = ClientListSerializer
    model = ClientModel
    decoder_ring = Secret()

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):
        # invalid_lookup_fields MUST contain " ," in the list for the exception message to be correct
        invalid_lookup_fields = ("name", "date_created", "date_modified", "id", "secret", " ,")
        if request.query_params and not [True for k in invalid_lookup_fields if
                                         request.query_params.dict().keys().__contains__(k)]:
            # The model.objects.filter will raise an exception if the user provides a field unknown to the model.
            #  Let's catch this and formulate ur own message on what a 'valid' field is
            try:
                # request.QueryDict is immutable, so copy the original QueryDict to mutable object
                self.query_params = request.query_params.copy()
                self.get_username(self.query_params)

                self.queryset = self.model.objects.filter(**self.query_params.dict())

                if self.queryset:
                    self.process_queryset()

            except exceptions.FieldError as e:
                ziplist_b = [''] * len(invalid_lookup_fields)
                zipped = zip(invalid_lookup_fields, ziplist_b)
                msg = e.args[0]

                # If wanting to see the exception stack trace then comment out the below return and Uncomment
                #   the below raise exceptions.FieldError section

                # <------ Production Usage Requires This Return Response ------>
                self.return_response = Response(["HTTP 400 BAD REQUEST", "{}".format(
                    reduce(lambda a, kv: a.replace(*kv), tuple(z for z in zipped), msg))],
                                                status=status.HTTP_400_BAD_REQUEST)

                # <--------- For Dev/Test Purposes Uncomment To View Stack Trace --------->
                # raise exceptions.FieldError(
                #     "{}".format(reduce(lambda a, kv: a.replace(*kv), tuple(z for z in zipped), msg)),
                #     status=status.HTTP_400_BAD_REQUEST)

        return self.return_response

    def get_username(self, query_params):

        for param in query_params:
            if param == 'secret__username':
                self.secret_user = query_params[param]
            elif param == 'username':
                self.secret_user = query_params[param]
                self.query_params.update({'secret__username': self.query_params.pop(param)[0]})

    def process_queryset(self):
        serializer_q = self.serializer_class(self.queryset, many=True)

        for data in serializer_q.data:
            for secret in data['secret']:
                # check if the username matches what the query suggests
                if secret['username'] == self.secret_user:
                    s = self.decoder_ring.password_packaging(
                        secret['password'], data['pubkey'], secret='dev')
                    secret['password'] = s
                else:
                    tmp = data['secret'].pop(data['secret'].index(secret))
        self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)


class CreateClientView(generics.CreateAPIView):

    queryset = ClientModel.objects.all()
    serializer_class = ClientCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


class UpdateClientView(generics.UpdateAPIView):
    pass


class AdminGetClientsView(generics.ListAPIView):

    serializer_class = ClientListSerializer
    model = ClientModel
    admin_model = AdminModel

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        if request.query_params and request.query_params['AdminId'] == os.environ['DJANGO_SECRET']:
            try:
                # control the admin features by whether or not the DJANGO_SECRET is added to the database as a client
                # if this get raises an error then the admin features are not enable
                # if this entry is in the database then the feature is enabled and we will return all entries
                admin_enabled = self.admin_model.objects.get(**request.query_params.dict())

                self.queryset = self.model.objects.all()
                serializer_q = self.serializer_class(self.queryset, many=True)
                self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
            except exceptions.ObjectDoesNotExist as e:
                self.return_response = Response(
                    ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])

        return self.return_response


class AdminGetSecretsView(generics.ListAPIView):

    serializer_class = SecretListSerializer
    model = SecretModel
    admin_model = AdminModel

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        if request.query_params and request.query_params['AdminId'] == os.environ['DJANGO_SECRET']:
            try:
                # control the admin features by whether or not the DJANGO_SECRET is added to the database as a client
                # if this get raises an error then the admin features are not enable
                # if this entry is in the database then the feature is enabled and we will return all entries
                admin_enabled = self.admin_model.objects.get(**request.query_params.dict())

                self.queryset = self.model.objects.all()
                serializer_q = self.serializer_class(self.queryset, many=True)
                self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
            except exceptions.ObjectDoesNotExist as e:
                self.return_response = Response(
                    ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])

        return self.return_response


class AdminGetClientView(generics.ListAPIView):

    serializer_class = ClientListSerializer
    model = ClientModel
    admin_model = AdminModel

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        if request.query_params and request.query_params['AdminId'] == os.environ['DJANGO_SECRET']:
            try:
                # control the admin features by whether or not the DJANGO_SECRET is added to the database as a client
                # if this get raises an error then the admin features are not enable
                # if this entry is in the database then the feature is enabled and we will return all entries

                admin_query = request.query_params.dict()
                admin_query.__delitem__('ClientId')
                self.query_params = request.query_params.dict()
                self.query_params.__delitem__('AdminId')

                admin_enabled = self.admin_model.objects.get(**admin_query)

                self.queryset = self.model.objects.filter(**self.query_params)
                serializer_q = self.serializer_class(self.queryset, many=True)
                self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
            except exceptions.ObjectDoesNotExist as e:
                self.return_response = Response(
                    ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])
            except exceptions.FieldError as e:
                self.return_response = Response(["HTTP 400 BAD REQUEST", "{}".format(e.args[0])])

        return self.return_response


class AdminGetSecretView(generics.ListAPIView):

    serializer_class = SecretListSerializer
    model = SecretModel
    admin_model = AdminModel

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        if request.query_params and request.query_params['AdminId'] == os.environ['DJANGO_SECRET']:
            try:
                # control the admin features by whether or not the DJANGO_SECRET is added to the database as a client
                # if this get raises an error then the admin features are not enable
                # if this entry is in the database then the feature is enabled and we will return all entries
                admin_query = request.query_params.dict()
                admin_query.__delitem__('Username')
                self.query_params = request.query_params.dict()
                self.query_params.__delitem__('AdminId')

                self.queryset = self.model.objects.filter(**self.query_params)
                serializer_q = self.serializer_class(self.queryset, many=True)
                self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
            except exceptions.ObjectDoesNotExist as e:
                self.return_response = Response(
                    ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])
            except exceptions.FieldError as e:
                self.return_response = Response(["HTTP 400 BAD REQUEST", "{}".format(e.args[0])])

        return self.return_response


class AdminGetSecretClientsView(generics.ListAPIView):

    serializer_class = AdminSecretClientListSerializer
    model = SecretModel
    admin_model = AdminModel

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        if request.query_params and request.query_params['AdminId'] == os.environ['DJANGO_SECRET']:
            try:
                # control the admin features by whether or not the DJANGO_SECRET is added to the database as a client
                # if this get raises an error then the admin features are not enable
                # if this entry is in the database then the feature is enabled and we will return all entries
                admin_query = request.query_params.dict()
                admin_query.__delitem__('Username')
                self.query_params = request.query_params.dict()
                self.query_params.__delitem__('AdminId')

                self.queryset = self.model.objects.filter(**self.query_params)
                serializer_q = self.serializer_class(self.queryset, many=True)
                self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
            except exceptions.ObjectDoesNotExist as e:
                self.return_response = Response(
                    ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])

        return self.return_response

    def delete(self, request, *args, **kwargs):

        if request.query_params and request.query_params['AdminId'] == os.environ['DJANGO_SECRET']:
            try:
                # control the admin features by whether or not the DJANGO_SECRET is added to the database as a client
                # if this get raises an error then the admin features are not enable
                # if this entry is in the database then the feature is enabled and we will return all entries
                admin_enabled = self.model.objects.get(**request.query_params.dict())

                #self.queryset = self.mode
                self.queryset.delete()
                # self.serializer_class.save()

            except exceptions.ObjectDoesNotExist as e:
                self.return_response = Response(
                    ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])

        return self.return_response


class AdminDeleteClient(generics.DestroyAPIView):

    serializer_class = ClientListSerializer
    model = ClientModel
    admin_model = AdminModel

    pass


class AdminDeleteSecret(generics.DestroyAPIView):

    serializer_class = SecretListSerializer
    model = SecretModel
    admin_model = AdminModel

    pass
