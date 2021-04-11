from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from logger import *
import os
import secrets
from crypto_side import *

class Car(CryptoSide):
    
    def execute_command(self):
        if self.command == 0:
            print('[car opened]')
        elif self.command == 1:
            print('[car closed]')
        else: 
            print('[unknown command]')

class Trinket(CryptoSide):
    def __init__(self, p_name):
        self.name = 'trinket-{}'.format(p_name)