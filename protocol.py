from logger import *

def register(p_trinket, p_car):
	p_car.set_side_pubkey(p_trinket)
	p_trinket.set_side_pubkey(p_car)
	print('0: (registration) {} (pubkey1 written to trinked), {} (pubkey2 written to car)'
		.format('key1','key2'))
	# 0: (registration) 0xXXXXXXXXXXXX (pubkey1 written to trinked), 0xXXXXXXXXXXXXXX (pubkey2 written to car)

def handshake(p_trinket, p_car):
	p_car.set_outer_challenge(p_trinket)
	p_car.set_command(p_trinket.get_command())
	print('[handshaked]')

def challenge(p_trinket, p_car):
	p_trinket.set_outer_challenge(p_car)
	p_trinket.check_confirmation(p_car)
	print('[challenged]')

def response(p_trinket, p_car):
	p_car.check_confirmation(p_trinket)
	print('[responsed]')
	p_car.execute_command()
	p_car.expire_challenges()
	p_trinket.expire_challenges()
	