from Crypto.PublicKey import RSA
from logger import *
import os

class Trinket:
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()
    car_key = ''

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()
        log('trinket keys reset')

    def set_car_key(self, p_trinket):
    	self.car_key = p_trinket.get_pubkey()