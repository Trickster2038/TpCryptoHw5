from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from logger import log
import os
import secrets

class CryptoSide:
    name = ''
    __secret_key = RSA.generate(1024, os.urandom)
    public_key = __secret_key.publickey()
    b_key = ''
    command = ''
    inner_challenge = ''

    def __init__(self, p_name):
        self.name = p_name

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        self.__secret_key = RSA.generate(1024, os.urandom)
        self.public_key = self.__secret_key.publickey()
        log('{} keys reset'.format(self.name))

    def set_side_pubkey(self, p_side_b):
        self.b_key = p_side_b.get_pubkey()




    def set_command(self, p_cmd):
        log('{} command set: {}'.format(self.name, p_cmd))
        self.command = p_cmd

    def get_command(self):
        return self.command

    def generate_challenge(self):
        #SHA256.new((command+challenge).encode())
        chg = secrets.token_hex(nbytes=256)
        self.inner_challenge = SHA256.new(chg.encode())
        log('{} challenge generated'.format(self.name))
        return self.inner_challenge



    def set_outer_challenge(self, p_side_b):
        self.outer_challenge = p_side_b.generate_challenge()
        log('{} got challenge'.format(self.name))

    def check_confirmation(self, p_side_b):
        b_sign = p_side_b.sign()
        log('{} checking sign...'.format(self.name))
        pkcs1_15.new(self.b_key).verify(self.inner_challenge, b_sign)
        # pkcs1_15.new(self.b_key).verify(self.inner_challenge, b_sign+b'x01') - check invalid



    def sign(self):
        signature = pkcs1_15.new(self.__secret_key).sign(self.outer_challenge)
        log('{} signed'.format(self.name))
        return signature



    def expire_challenges(self):
        self.inner_challenge = ''
        self.outer_challenge = ''
        log('{} challenges expired'.format(self.name))