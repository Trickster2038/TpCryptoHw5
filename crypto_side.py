#from Crypto.PublicKey import RSA
#from Crypto.Signature import pkcs1_15
import rsa
from Crypto.Hash import SHA256
from logger import Logger
import os
import secrets
import random

class VerifyError(Exception):
    discription = 'signature not verified'

class ChallengeMsg:
    content = ''

    def __init__(self, p_num):
        self.content = str(p_num).encode()

    def read(self, x):
        return self.content

class CryptoSide:
    name = ''
    # how to generate new?
    #e= int(random.uniform(65557, 65557*2))
    #__secret_key = RSA.generate(1024, os.urandom) # os.urandom
    #public_key = __secret_key.publickey()
    (__secret_key, public_key) = rsa.newkeys(1024)
    b_key = ''
    command = ''
    inner_challenge = ''

    def __init__(self, p_name):
        self.name = p_name

    def get_pubkey(self):
        return self.public_key

    def reset_keys(self):
        # self.__secret_key = RSA.generate(1024, os.urandom)
        # self.public_key = self.__secret_key.publickey()
        (self.public_key, self.__secret_key) = rsa.newkeys(512)
        Logger.log('{} keys reset'.format(self.name))

    def set_side_pubkey(self, p_side_b):
        self.b_key = p_side_b.get_pubkey()




    def set_command(self, p_cmd):
        Logger.log('{} command set: {}'.format(self.name, p_cmd))
        self.command = p_cmd

    def get_command(self):
        return self.command

    def generate_challenge(self):
        #SHA256.new((command+challenge).encode())
        chg = secrets.token_hex(nbytes=256)
        self.inner_challenge = ChallengeMsg(SHA256.new(chg.encode()))
        Logger.log('{} challenge generated'.format(self.name))
        return self.inner_challenge



    def set_outer_challenge(self, p_side_b):
        self.outer_challenge = p_side_b.generate_challenge()
        Logger.log('{} got challenge'.format(self.name))

    def check_confirmation(self, p_side_b):
        Logger.log('{} prepare to sign...'.format(self.name))
        b_sign = p_side_b.sign()
        Logger.log('{} checking sign...'.format(self.name))
        try:
            #pkcs1_15.new(self.b_key).verify(self.inner_challenge, b_sign)
            rsa.verify(self.inner_challenge, b_sign, self.b_key)
        except: 
            raise VerifyError('unverified signature')
        # pkcs1_15.new(self.b_key).verify(self.inner_challenge, b_sign+b'x01') - check invalid



    def sign(self):
        #signature = pkcs1_15.new(self.__secret_key).sign(self.outer_challenge)
        signature = rsa.sign(self.outer_challenge, self.__secret_key, 'SHA-1')
        Logger.log('{} signed'.format(self.name))
        return signature



    def expire_challenges(self):
        self.inner_challenge = ''
        self.outer_challenge = ''
        Logger.log('{} challenges expired'.format(self.name))