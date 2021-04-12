from vehicles import Car
from vehicles import Trinket
from protocol import *
from logger import *
from crypto_side import *


if __name__ == '__main__':

	# turns logger off, on - 1
	Logger.config(0)

	# initialize sides
	car_alice = Car('Camry 3.5')
	trinket_bob = Trinket('Bob')
	trinket_eva = Trinket('Eva')

	# reset crypto-keys (public and secret)
	car_alice.reset_keys()
	trinket_bob.reset_keys()
	trinket_eva.reset_keys()

	# creating car-trinket pair
	register(trinket_bob, car_alice)

	# test of closing car
	print('\n===== TEST: Bob, Alice, close =====\n')
	trinket_bob.set_command(1) # 0 - open, 1 - close, other - unknown
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)

	print('\n===== TEST: Bob, Alice, open =====\n')
	trinket_bob.set_command(0) # 0 - open, 1 - close, other - unknown
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)

	print('\n===== TEST: Bob, Alice, unkonwn =====\n')
	trinket_bob.set_command(6) # 0 - open, 1 - close, other - unknown
	handshake(trinket_bob, car_alice)
	challenge(trinket_bob, car_alice)
	response(trinket_bob, car_alice)

	# test of sabotaging protocol by Eva
	try:
		print('\n===== TEST: Bob, Eva, open =====\n')
		trinket_bob.set_command(0) # 0 - open, 1 - close, other - unknown
		handshake(trinket_bob, car_alice)
		challenge(trinket_eva, car_alice)
		response(trinket_bob, car_alice)
	except VerifyError as e:
		print('{}'.format(repr(e)))

	# test of sabotaging protocol by re-use of command
	try:
		print('\n===== TEST: Bob, Alice, open x2 =====\n')
		trinket_bob.set_command(0) # 0 - open, 1 - close, other - unknown
		handshake(trinket_bob, car_alice)
		challenge(trinket_bob, car_alice)
		response(trinket_bob, car_alice)
		response(trinket_bob, car_alice)
	except VerifyError as e:
		print('{}'.format(repr(e)))