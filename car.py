from Crypto.PublicKey import RSA
from logger import *
import os

class Car:
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()
    trinket_key = ''

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()
        log('car keys reset')

    def set_trinket_key(self, p_car):
        self.trinket_key = p_car.get_pubkey()