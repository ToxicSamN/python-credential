
import hashlib
from pycrypt.encryption import Encryption


class Client:
    """
        Still TBD on what this will be used for if at all.
    """

    def __init__(self, model, ClientId):
        self.model = model
        self.client_id = ClientId
        self.data = None
        super().__init__()

    @staticmethod
    def create_clientid(string_data):
        hsh = hashlib.sha512(string_data.encode())
        return hsh.hexdigest()

    def validate(self):
        self.data = self.model.objects.filter(ClientId=self.client_id)
        if not self.data:
            return None
        else:
            self.data = self.data[0]
            return True
