# api/views.py

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
from.decorators import admin_login_required, create_login_required, update_login_required, retrieve_login_required
from .render import CredStoreBrowsableAPIRenderer

from .pystuffing.secret import Secret


class ModelFieldError(exceptions.FieldError):
    pass


@method_decorator(retrieve_login_required, name='dispatch')
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
            #  Let's catch this and formulate our own message on what a 'valid' field is
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
                        # TODO: change the dev value to production of settings.SECRET
                        # TODO: Better yet make this a hash of the HTTPS Certificate thumbprint of the server
                        secret['password'], data['pubkey'], secret='dev')
                    secret['password'] = s
                else:
                    tmp = data['secret'].pop(data['secret'].index(secret))
        self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)


@method_decorator(update_login_required, name='dispatch')
class UpdateCredentialView(generics.UpdateAPIView):
    """ Not yet built out"""
    pass


@method_decorator(admin_login_required, name='dispatch')
class DeleteCredentialView(generics.DestroyAPIView):
    """ Not yet built out"""
    pass


@method_decorator(admin_login_required, name='dispatch')
class UpdateSecretView(generics.UpdateAPIView):
    """ Not yet built out"""
    pass


@method_decorator(admin_login_required, name='dispatch')
class DeleteSecretView(generics.DestroyAPIView):
    """ Not yet built out"""
    pass


@method_decorator(admin_login_required, name='dispatch')
class UpdateUserAccessView(generics.UpdateAPIView):
    """ Not yet built out"""
    pass


@method_decorator(admin_login_required, name='dispatch')
class AdminGetClientsView(generics.ListAPIView):

    serializer_class = AdminClientListSerializer
    model = ClientModel
    renderer_classes = [CredStoreBrowsableAPIRenderer]

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):
        try:
            self.queryset = self.model.objects.all()
            serializer_q = self.serializer_class(self.queryset, many=True)
            self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])

        return self.return_response


@method_decorator(admin_login_required, name='dispatch')
class AdminGetSecretsView(generics.ListAPIView):

    serializer_class = AdminSecretSerializer
    model = SecretModel
    renderer_classes = [CredStoreBrowsableAPIRenderer]

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        try:
            self.queryset = self.model.objects.all()
            serializer_q = self.serializer_class(self.queryset, many=True)
            self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])

        return self.return_response


@method_decorator(admin_login_required, name='dispatch')
class AdminGetClientView(generics.ListAPIView):

    serializer_class = AdminClientListSerializer
    model = ClientModel
    renderer_classes = [CredStoreBrowsableAPIRenderer]

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        try:
            self.query_params = request.query_params.dict()
            self.queryset = self.model.objects.filter(**self.query_params)
            serializer_q = self.serializer_class(self.queryset, many=True)
            self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Object Not Found")])
        except exceptions.FieldError as e:
            self.return_response = Response(["HTTP 400 BAD REQUEST", "{}".format(e.args[0])])

        return self.return_response


@method_decorator(admin_login_required, name='dispatch')
class AdminGetSecretView(generics.ListAPIView):

    serializer_class = AdminSecretSerializer
    model = SecretModel
    renderer_classes = [CredStoreBrowsableAPIRenderer]

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        try:
            self.query_params = request.query_params.dict()

            self.queryset = self.model.objects.filter(**self.query_params)
            serializer_q = self.serializer_class(self.queryset, many=True)
            self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Admin Only features have not been enabled")])
        except exceptions.FieldError as e:
            self.return_response = Response(["HTTP 400 BAD REQUEST", "{}".format(e.args[0])])

        return self.return_response


@method_decorator(admin_login_required, name='dispatch')
class AdminGetSecretClientsView(generics.ListAPIView):

    serializer_class = AdminSecretClientListSerializer
    model = SecretModel
    renderer_classes = [CredStoreBrowsableAPIRenderer]

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):

        try:
            self.query_params = request.query_params.dict()

            self.queryset = self.model.objects.filter(**self.query_params)
            serializer_q = self.serializer_class(self.queryset, many=True)
            self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Object Not Found")])

        return self.return_response


@method_decorator(admin_login_required, name='dispatch')
class AdminDeleteClient(generics.DestroyAPIView):

    serializer_class = ClientListSerializer
    model = ClientModel

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def destroy(self, request, *args, **kwargs):

        try:
            self.query_params = request.query_params.dict()

            self.queryset = self.model.objects.get(**self.query_params)
            self.perform_destroy(self.queryset)
            self.return_response = Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Object Not Found")])

        return self.return_response


@method_decorator(admin_login_required, name='dispatch')
class AdminDeleteSecret(generics.DestroyAPIView):

    serializer_class = SecretListSerializer
    model = SecretModel

    def __init__(self):
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def destroy(self, request, *args, **kwargs):

        try:
            self.query_params = request.query_params.dict()

            self.queryset = self.model.objects.get(**self.query_params)
            self.perform_destroy(self.queryset)
            self.return_response = Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.ObjectDoesNotExist as e:
            self.return_response = Response(
                ["HTTP 400 BAD REQUEST", "{}".format("Object Not Found")])

        return self.return_response
