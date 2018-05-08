from django.db import models


class Secret(models.Model):
    """This is the class for the Secret model"""
    username = models.CharFild(blank=False, unique=True)
    password = models.CharField(blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return the Human Readable representation of the model"""
        return "Username: {}\nDate Created:{}\Date Modified:{}".format(self.username,
                                                                       self.date_created,
                                                                       self.date_modified)

class Client(models.Model):
    id = models.CharFild(blank=False, unique=True)
    pubkey = models.CharFild(blank=False, unique=True)