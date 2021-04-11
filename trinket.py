from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
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
        #SHA256.new((command+challenge).encode())
        chg = secrets.token_hex(nbytes=256)
        self.inner_challenge = SHA256.new(chg.encode())
        log('trinket challenge generated')
        return self.inner_challenge



    def set_outer_challenge(self, p_car):
        self.outer_challenge = p_car.generate_challenge()
        log('trinket got challenge')

    def check_confirmation(self, p_car):
        car_sign = p_car.sign()
        log('trinket checking sign...')
        pkcs1_15.new(self.car_key).verify(self.inner_challenge, car_sign)
        # pkcs1_15.new(self.car_key).verify(self.inner_challenge, car_sign+b'x01') - check invalid



    def sign(self):
        signature = pkcs1_15.new(self.__secret_key).sign(self.outer_challenge)
        log('trnket signed')
        return signature



    def expire_challenges(self):
        self.inner_challenge = ''
        self.outer_challenge = ''
        log('trinket challenges expired')