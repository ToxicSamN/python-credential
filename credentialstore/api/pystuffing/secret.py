import os
import base64
from pycrypt.encryption import Encryption
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class Secret(Encryption):
    """
        This class is iherited from the Encryption class and is used
        specifically for encrypting and decrypting the passwords for the clients
    """

    def __init__(self):
        self.server_priv_file = os.environ['RSA_PRIV']
        self.server_pub_file = os.environ['RSA_PUB']
        super().__init__()

    def encrypt(self, privateData, publickey=None, output_file=None):
        """
        Override encrypt method to accept a public key as a string instead of a public key file

        :param privateData: Clear text data to be encrypted
        :param publickey: public key string (optional if using publickey_file)
        :param output_file: Output the encrypted string to a file (optional)
        :return: None
        """

        if not publickey:
            # no public key was provided so will use the global public key
            with open(self.server_pub_file, 'rb') as f:
                publickey = f.read()
                f.close()

        if type(privateData) is str:
            privateData = privateData.encode("utf-8")

        pubkey = RSA.import_key(publickey)
        cipher_rsa = PKCS1_OAEP.new(pubkey)
        encrypted_message = cipher_rsa.encrypt(privateData)

        self._Encryption__decrypted_message = None
        self._Encryption__encrypted_message = base64.b64encode(encrypted_message)

    def password_packaging(self, encrypted_data, client_public_key,
                           secret=os.environ['DJANGO_SECRET']):
        """
        This method is used to decrypt a given password using the server-side private key
        and re-encrypting the password with a generated shared key. Then encrypt the shared
        key with the clients public key.
        :param encrypted_data: Server-Side Encrypted password
        :param client_public_key: Client PublicKey in the form of a file name or a string
        :param secret: The Secret Key to the Private Key for Decryption process
        :return: Re-Encrypted Message
        """

        self.decrypt(private_key_file=self.server_priv_file,
                     encrypted_data=encrypted_data,
                     secret_code=secret)

        shared_key = RSA.generate(2048)
        private = shared_key.exportKey(pkcs=8,
                                       protection="scryptAndAES256-CBC")

        # Encrypt the password with the new shared key
        self.encrypt(privateData=self.get_decrypted_message(),
                     publickey=private)
        enc_pwd = self.get_encrypted_message()

        # Encrypt the shared private key with the client's public key
        self.encrypt(privateData=private,
                     publickey=client_public_key)
        enc_key = self.get_encrypted_message()

        return {'password': enc_pwd,
                'shared_key': enc_key,
                }
