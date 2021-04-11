from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from logger import log
import os
import secrets
from crypto_side import CryptoSide

class Car(CryptoSide):
    
    def execute_command(self):
        if self.command == 0:
            log('[car opened]')
        elif self.command == 1:
            log('[car closed]')
        else: 
            log('[unknown command]')

class Trinket(CryptoSide):
    def __init__(self):
        self.name = 'trinket'