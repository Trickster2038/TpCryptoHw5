#from Crypto.Hash import SHA256
#from Crypto.PublicKey import RSA
#from Crypto.Signature import pkcs1_15
#import os

# pip intall pycryptodome
# pip install pycryptodomex
# print(a.get_pubkey().export_key().decode())
# a ={'av':4,'bn':5} 
# a['av'] == 4

from vehicles import Car
from vehicles import Trinket
from protocol import *
from logger import log


if __name__ == '__main__':
	car_alice = Car('Camry 3.5')
	trinket_bob = Trinket()
	car_alice.reset_keys()
	trinket_bob.reset_keys()
	register(trinket_bob, car_alice)
	trinket_bob.set_command(1)
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)
