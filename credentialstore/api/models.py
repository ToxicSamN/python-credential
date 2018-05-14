# api/models.py

from django.db import models
from rest_framework import serializers


class Secret(models.Model):
    """
    This is the class for the Secret model
    """
    username = models.CharField(max_length=65535, blank=False, unique=True)
    password = models.CharField(max_length=65535, blank=False, unique=True, )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the Human Readable representation of the model
        """
        return "Username: {}\nDate Created:{}\Date Modified:{}".format(self.username,
                                                                       self.date_created,
                                                                       self.date_modified)


class Client(models.Model):
    """
    This is the class for the Client model
    """
    ClientId = models.CharField(max_length=65535, blank=False, unique=True)
    pubkey = models.TextField(max_length=65535, blank=False, unique=True)
    name = models.CharField(max_length=65535, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the Human Readable representation of the model
        """
        return "ID: {}\nPublicKey: {}".format(self.id, self.pubkey)
