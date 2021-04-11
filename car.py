from Crypto.PublicKey import RSA
from logger import *
import os
import secrets

class Car:
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()
    trinket_key = ''
    outer_challenge = ''
    command = ''

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()
        log('car keys reset')

    def set_trinket_key(self, p_car):
        self.trinket_key = p_car.get_pubkey()

    # def sign(self, p_chg):
    #     signature = pkcs1_15.new(self.__secret_key).sign(hash)
    #     return signature 

    def set_outer_challenge(self, p_trinket):
        self.outer_challenge = p_trinket.generate_challenge()
        log('car got challenge')

    def set_command(self, p_trinket):
        self.command = p_trinket.get_command()
        log('car got cmd: {}'.format(self.command))