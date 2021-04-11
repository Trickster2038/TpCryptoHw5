#from Crypto.Hash import SHA256
#from Crypto.PublicKey import RSA
#from Crypto.Signature import pkcs1_15
#import os

# pip intall pycryptodome
# pip install pycryptodomex

from car import *
from trinket import *
from protocol import *


if __name__ == '__main__':
	car_alice = Car()
	trinket_bob = Trinket()
	car_alice.reset_keys()
	trinket_bob.reset_keys()
	register(trinket_bob, car_alice)
