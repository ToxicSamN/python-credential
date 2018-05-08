from django.db import models


class Secret(models.Model):
    """This is the class for the Secret model"""
    username = models.CharField(blank=False, unique=True)
    password = models.CharField(blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return the Human Readable representation of the model"""
        return "Username: {}\nDate Created:{}\Date Modified:{}".format(self.username,
                                                                       self.date_created,
                                                                       self.date_modified)


class Client(models.Model):
    """This is the class for the Client model"""
    id = models.CharField(blank=False, unique=True)
    pubkey = models.CharField(blank=False, unique=True)
    name = models.CharField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return the Human Readable representation of the model"""
        return "ID: {}\nPublicKey: {}".format(self.id, self.pubkey)
