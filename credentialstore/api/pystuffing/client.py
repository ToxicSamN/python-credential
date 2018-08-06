# pystuffing/client.py

import hashlib
import random


class Client:
    """
        Still TBD on what this will be used for if at all.
    """

    @staticmethod
    def create_clientid():
        hsh = hashlib.sha512(random._urandom(4096))
        return hsh.hexdigest()
