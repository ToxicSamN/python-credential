# api/models.py

from django.db import models
from django.core import exceptions
from .widgets import PasswordModelField


class SecretModel(models.Model):
    """
    This is the class for the Secret model
    """
    username = models.CharField(max_length=65535, blank=False, unique=True)
    password = PasswordModelField(max_length=65535, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the Human Readable representation of the model
        """
        return "Username: {}\nDate Created:{}\Date Modified:{}".format(self.username,
                                                                       self.date_created,
                                                                       self.date_modified)

    def validate_username(self, username):
        try:
            query_set = self.objects.get(username=username)
            return True
        except exceptions.ObjectDoesNotExist as err:
            raise exceptions.ObjectDoesNotExist(
                "No username '{}' exists in database.".format(username))


class ClientModel(models.Model):
    """
    This is the class for the Client model
    """
    ClientId = models.CharField(max_length=65535, blank=False, unique=True)
    pubkey = models.TextField(max_length=65535, blank=False, unique=True)
    name = models.CharField(max_length=65535, blank=False)
    secret = models.ManyToManyField(SecretModel, related_name='clients')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the Human Readable representation of the model
        """
        return "ID: {}\nPublicKey: {}".format(self.id, self.pubkey)
