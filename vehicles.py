from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from logger import *
import os
import secrets
from crypto_side import *

'''
This module implements 2 classes: Car and Trinket,
which are inherited from abstract class 'crypto_side.CryptoSide'
(CryptoSide emulates participant of 'handshake' protocol)
'''

class Car(CryptoSide):
    
    def execute_command(self):
        '''In addition to functions of CryptoSide
        Car can execute some commands, transfered
        in 'handshake protocol'
        '''
        if self.command == 0:
            print('4: (action) car: opened')
        elif self.command == 1:
            print('4: (action) car: closed')
        else: 
            print('4: (action) car: do nothing (unknown command id)')

class Trinket(CryptoSide):
    def __init__(self, p_name):
        self.name = 'trinket-{}'.format(p_name)