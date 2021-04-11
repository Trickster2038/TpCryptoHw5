from Crypto.PublicKey import RSA
from logger import *
import os
import secrets

class Trinket:
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()
    car_key = ''
    command = ''
    inner_challenge = ''

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()
        log('trinket keys reset')

    def set_car_key(self, p_trinket):
    	self.car_key = p_trinket.get_pubkey()

    def set_command(self, p_cmd):
    	log('trinket command set: {}'.format(p_cmd))
    	self.command = p_cmd

    def get_command(self):
    	return self.command

    def generate_challenge(self):
    	self.inner_challenge = secrets.token_hex(nbytes=256)
    	log('trinket challenge generated')
    	return self.inner_challenge

    def expire_challenge(self):
    	self.inner_challenge = ''
    	log('trinket challenge expired')