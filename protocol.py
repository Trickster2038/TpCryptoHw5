from logger import *

def register(p_trinket, p_car):
	p_car.set_side_pubkey(p_trinket)
	p_trinket.set_side_pubkey(p_car)
	log('[registered]')

def handshake(p_trinket, p_car):
	p_car.set_outer_challenge(p_trinket)
	p_car.set_command(p_trinket.get_command())
	log('[handshaked]')

def challenge(p_trinket, p_car):
	p_trinket.set_outer_challenge(p_car)
	p_trinket.check_confirmation(p_car)
	log('[challenged]')

def response(p_trinket, p_car):
	p_car.check_confirmation(p_trinket)
	log('[responsed]')
	p_car.execute_command()
	p_car.expire_challenges()
	p_trinket.expire_challenges()
	