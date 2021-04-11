from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from logger import *
import os
import secrets

class Car:
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()
    trinket_key = ''
    outer_challenge = ''
    command = ''
    inner_challenge = ''

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()
        log('car keys reset')

    def set_trinket_key(self, p_car):
        self.trinket_key = p_car.get_pubkey()   




    def set_outer_challenge(self, p_trinket):
        self.outer_challenge = p_trinket.generate_challenge()
        log('car got challenge')

    def set_command(self, p_trinket):
        self.command = p_trinket.get_command()
        log('car got cmd: {}'.format(self.command))



    def sign(self):
        signature = pkcs1_15.new(self.__secret_key).sign(self.outer_challenge)
        log('car signed')
        return signature

    def generate_challenge(self):
        chg = secrets.token_hex(nbytes=256)
        self.inner_challenge = SHA256.new(chg.encode())
        log('car challenge generated')
        return self.inner_challenge



    def check_confirmation(self, p_trinket):
        trinket_sign = p_trinket.sign()
        log('car checking sign...')
        pkcs1_15.new(self.trinket_key).verify(self.inner_challenge, trinket_sign)
        # pkcs1_15.new(self.car_key).verify(self.inner_challenge, car_sign+b'x01') - check invalid



    def expire_challenges(self):
        self.inner_challenge = ''
        self.outer_challenge = ''
        log('cars challenges expired')

    def execute_command(self):
        if self.command == 0:
            log('[car opened]')
        elif self.command == 1:
            log('[car closed]')
        else: 
            log('[unknown command]')