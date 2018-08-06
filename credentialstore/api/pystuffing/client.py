# pystuffing/client.py

import hashlib


class Client:
    """
        Still TBD on what this will be used for if at all.
    """

    @staticmethod
    def create_clientid(string_data):
        hsh = hashlib.sha512(string_data.encode())
        return hsh.hexdigest()
