# api/views.py

import json
from functools import reduce
from django.shortcuts import render
from django.core import serializers, exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ClientListSerializer, ClientCreateSerializer, SecretListSerializer, SecretCreateSerializer
from .models import ClientModel, SecretModel
from .pystuffing.secret import Secret
from .pystuffing.client import Client


class RealClientListView(generics.ListAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientListSerializer
    decoder_ring = Secret()

    def get(self, request, *args, **kwargs):
        # invalid_lookup_fields MUST contain " ," in the list for the exception message to be correct
        invalid_lookup_fields = ("name", "date_created", "date_modified", "id", "secret", " ,")
        if request.query_params and not [True for k in invalid_lookup_fields if
                                         request.query_params.dict().keys().__contains__(k)]:
            # The model.objects.filter will raise an exception if the user provides a field unknown to the model.
            #  Let's catch this and formulate ur own message on what a 'valid' field is
            try:
                # request.QueryDict is immutable, so copy the original QueryDict to mutable object
                query_params = request.query_params.copy()

                for param in request.query_params:
                    if param == 'secret__username':
                        secret_user = request.query_params[param]
                    elif param == 'username':
                        secret_user = request.query_params[param]
                        query_params.update({'secret__username': query_params.pop(param)[0]})
                    else:
                        secret_user = 'null'

                queryset = ClientModel.objects.filter(**query_params.dict())
                # queryset = ClientModel.objects.filter(**request.query_params.dict())
            except exceptions.FieldError as e:
                ziplist_b = [''] * len(invalid_lookup_fields)
                zipped = zip(invalid_lookup_fields, ziplist_b)
                msg = e.args[0]

                # If wanting to see the exception stack trace then comment out the below return and Uncomment
                #   the below raise exceptions.FieldError section

                # <------ Production Usage Requires This Return Response ------>
                return Response(["HTTP 400 BAD REQUEST",
                                 "{}".format(reduce(lambda a, kv: a.replace(*kv), tuple(z for z in zipped), msg))],
                                status=status.HTTP_400_BAD_REQUEST)

                # <--------- For Dev/Test Purposes Uncomment To View Stack Trace --------->
                # raise exceptions.FieldError(
                #     "{}".format(reduce(lambda a, kv: a.replace(*kv), tuple(z for z in zipped), msg)),
                #     status=status.HTTP_400_BAD_REQUEST)

            if queryset:
                serializer_q = ClientListSerializer(queryset, many=True)
                # ClientModel.validate_user_access(ClientModel, secret_user[0])
                for data in serializer_q.data:
                    for secret in data['secret']:
                        # check if the username matches what the query suggests
                        if secret['username'] == secret_user:
                            s = self.decoder_ring.password_packaging(
                                secret['password'], data['pubkey'], secret='dev')
                            secret['password'] = s
                        else:
                            tmp = data['secret'].pop(data['secret'].index(secret))
                return Response(serializer_q.data, status=status.HTTP_200_OK)

        return Response(["HTTP 400 BAD REQUEST", "Must provide a valid query"], status=status.HTTP_400_BAD_REQUEST)



class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientListSerializer
    lookup_field = 'ClientId'


class ClientListView(generics.CreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = ClientModel.objects.all()
    serializer_class = ClientListSerializer

    def create(self, request, *args, **kwargs):
        client_id = None

        if request.data.get('string_data'):
            client_id = Client.create_clientid(request.data['string_data'])
        elif request.data.get('ClientId'):
            client_id = request.data['ClientId']

        client = Client(ClientModel, ClientId=client_id)
        if not client.validate():
            return Response(['HTTP 400 BAD REQUEST. Server does not exist', request.data])

        return Response(['HTTP 200 OK',
                         {'PublicKey': client.data.pubkey,
                          'ClientName': client.data.name
                         }
                        ],
                        status=status.HTTP_200_OK)


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
