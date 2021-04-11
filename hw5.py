# pip intall pycryptodome
# pip install pycryptodomex
# print(a.get_pubkey().export_key().decode())
# a ={'av':4,'bn':5} 
# a['av'] == 4

from vehicles import Car
from vehicles import Trinket
from protocol import *
from logger import *
from crypto_side import *


if __name__ == '__main__':

	Logger.config(0)

	car_alice = Car('Camry 3.5')
	trinket_bob = Trinket('Bob')
	trinket_eva = Trinket('Eva')

	car_alice.reset_keys()
	trinket_bob.reset_keys()
	trinket_eva.reset_keys()

	register(trinket_bob, car_alice)

	print('\n=== TEST: Bob, Alice, close ===\n')
	trinket_bob.set_command(1)
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)

	print('\n=== TEST: Bob, Alice, open ===\n')
	trinket_bob.set_command(0)
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)

	print('\n=== TEST: Bob, Alice, unkonwn ===\n')
	trinket_bob.set_command(6)
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)

	try:
		print('\n=== TEST: Bob, Eva, open ===\n')
		trinket_bob.set_command(0)
		handshake(trinket_bob, car_alice)
		challenge(trinket_eva, car_alice)
		response(trinket_bob, car_alice)
	except VerifyError as e:
		print('\n{}'.format(repr(e)))

	try:
		print('\n=== TEST: Bob, Alice, open x2 ===\n')
		trinket_bob.set_command(0)
		handshake(trinket_bob, car_alice)
		challenge(trinket_bob, car_alice)
		response(trinket_bob, car_alice)
		response(trinket_bob, car_alice)
	except VerifyError as e:
		print('\n{}'.format(repr(e)))