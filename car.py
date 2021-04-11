from Crypto.PublicKey import RSA
import os

class Car:
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()