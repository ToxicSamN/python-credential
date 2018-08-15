# api/views.py

import os
from functools import reduce
from django.core import exceptions
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ClientListSerializer, SecretListSerializer, ClientCreateSerializer
from .serializers import AdminClientListSerializer, AdminSecretClientListSerializer, AdminSecretSerializer
from .models import ClientModel, SecretModel
from.decorators import admin_login_required, create_login_required, update_login_required, retrieve_login_required
from .render import CredStoreBrowsableAPIRenderer
from .pystuffing.secret import Secret
from .pystuffing.client import Client


class ModelFieldError(exceptions.FieldError):
    pass


class NewClientId(generics.ListAPIView):

    def __init__(self):
        self.client_id = Client().create_clientid()
        super().__init__()

    def get(self, request, *args, **kwargs):
        return Response({"ClientId": self.client_id}, status=status.HTTP_200_OK)


class GetCredentialView(generics.ListAPIView):
    """
        Model View for GetCredential requests
    """

    serializer_class = ClientListSerializer
    model = ClientModel
    # decoder_ring is the heart of encrypting and decrypting the passwords that are returned
    decoder_ring = Secret()

    def __init__(self):
        self.secret_user = 'null'
        self.query_params = None
        self.return_response = Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"],
                                        status=status.HTTP_400_BAD_REQUEST)
        super().__init__()

    def get(self, request, *args, **kwargs):
        """
        Overriden get method to allow for url query parameter checking and validation
        as well as decrypting password with server-side priv key and re-encrypting
        with client-side pub key.
        :param request: HTTP Request submitted by the user
        :param args: args
        :param kwargs: kwargs
        :return: HTTPResponse
        """
        # invalid_lookup_fields MUST contain " ," in the list for the exception message to be correct
        invalid_lookup_fields = ("name", "date_created", "date_modified", "id", "secret", " ,")
        if request.query_params and not [True for k in invalid_lookup_fields if
                                         request.query_params.dict().keys().__contains__(k)]:
            # The model.objects.filter will raise an exception if the user provides a field unknown to the model.
            #  Let's catch this and formulate our own message on what a 'valid' field is otherwise
            #  the default message will indicate valid fields that aren't actually valid.
            try:
                # request.QueryDict is immutable, so copy the original QueryDict to mutable object
                self.query_params = request.query_params.copy()
                self.get_username(self.query_params)

                # get the queryset from the model
                self.queryset = self.model.objects.filter(**self.query_params.dict())

                # if there was a valid object returned then process the queryset
                if self.queryset:
                    self.process_queryset()

            except exceptions.FieldError as e:
                # There was an issue so now we need to formulate the error message we want to return to the user,
                # while not giving away too much information

                # create an empty array of the size of invalid_lookup_fields so that we can run zip
                ziplist_b = [''] * len(invalid_lookup_fields)
                zipped = zip(invalid_lookup_fields, ziplist_b)
                msg = e.args[0]

                # If wanting to see the exception stack trace then comment out the below return and Uncomment
                #   the below raise exceptions.FieldError section

                # <------ Production Usage Requires This Return Response ------>
                #  Run reduce to filter out all of the invalid_lookup_fields from the msg string
                self.return_response = Response(["HTTP 400 BAD REQUEST", "{}".format(
                    reduce(lambda a, kv: a.replace(*kv), tuple(z for z in zipped), msg))],
                                                status=status.HTTP_400_BAD_REQUEST)

                # <--------- For Dev/Test Purposes Uncomment To View Stack Trace --------->
                # raise exceptions.FieldError(
                #     "{}".format(reduce(lambda a, kv: a.replace(*kv), tuple(z for z in zipped), msg)),
                #     status=status.HTTP_400_BAD_REQUEST)

        return self.return_response

    def get_username(self, query_params):
        """
        Method for searching through the request paramaters for secret__username or username
        :param query_params: Request Query Parameter from the request sent by the client
        :return: None
        """
        for param in query_params:
            # Look for parameter secret__username since this is a valid query as well and is preceisley
            #  how we are able to query through the client model and return the secret object from the secret model
            if param == 'secret__username':
                self.secret_user = query_params[param]
            # if the query parameter is just username then pull out the username and formulate the model query
            # needed to get the secret object from the secret model.
            elif param == 'username':
                self.secret_user = query_params[param]
                self.query_params.update({'secret__username': self.query_params.pop(param)[0]})

    def process_queryset(self):
        """
        This method is used to serialize the data, then pull out the password and send it
        through the Secret().decrypt()/Secret().encrypt() methods. First decrypting the
        encrypted password with the server-side private RSA key. Second, using the public
        key of the client requesting the credentials, re-encrypt the password and store
        this result in the serialized data fro return back to the client.
        :return: None
        """

        # send the queryset to be serialized
        serializer_q = self.serializer_class(self.queryset, many=True)

        # loop through the serialized data looking for the secret model information
        for data in serializer_q.data:
            # loop through the serialized secret data looking for the username and password
            for secret in data['secret']:
                # check if the username matches what the query suggests
                if secret['username'] == self.secret_user:
                    # Run the password_packaging method on the password using the pubkey returned
                    #  from the serializer_q
                    s = self.decoder_ring.password_packaging(
                        secret['password'], data['pubkey'], secret=os.environ['DJANGO_SECRET'])
                    # set the password data to the string encrypted by the client pubkey
                    secret['password'] = s
                else:
                    tmp = data['secret'].pop(data['secret'].index(secret))
        self.return_response = Response(serializer_q.data, status=status.HTTP_200_OK)


@method_decorator(update_login_required, name='dispatch')
class UpdateCredentialView(generics.UpdateAPIView):
    """ Not yet built out, for future relase """
    pass


@method_decorator(admin_login_required, name='dispatch')
class DeleteCredentialView(generics.DestroyAPIView):
    """ Not yet built out, for future relase """
    pass


@method_decorator(admin_login_required, name='dispatch')
class UpdateSecretView(generics.UpdateAPIView):
    """ Not yet built out, for future relase """
    pass


@method_decorator(admin_login_required, name='dispatch')
class DeleteSecretView(generics.DestroyAPIView):
    """ Not yet built out, for future relase """
    pass


@method_decorator(admin_login_required, name='dispatch')
class UpdateUserAccessView(generics.UpdateAPIView):
    """ Not yet built out, for future relase """
    pass


@method_decorator(admin_login_required, name='dispatch')
class AdminGetClientsView(generics.ListAPIView):
    """
        Admin view for retrieving clients
    """

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
    """
        Admin view for retrieving usernames/passwords
    """

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
    """
    Admin view for retrieving a single client
    """

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
    """
        Admin view for retrieving a single username/password
    """

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
    """
        Admin view for retrieving clients and all associated usernames/passwords each client has access to
    """

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
    """
        Admin view for Deleting a single client
    """

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
    """
        Admin view for deleting a single client
    """

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
