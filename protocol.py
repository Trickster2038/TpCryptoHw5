from car import Car
from trinket import Trinket
from logger import *

def register(p_trinket, p_car):
	p_car.set_trinket_key(p_trinket)
	p_trinket.set_car_key(p_car)
	log('[registered]')

def handshake(p_trinket, p_car):
	p_car.set_outer_challenge(p_trinket)
	p_car.set_command(p_trinket)
	log('[handshaked]')

def challenge(p_trinket, p_car):
	p_trinket.set_outer_challenge(p_car)
	p_trinket.check_confirmation(p_car)
	log('[challenged]')

def response(p_trinket, p_car):
	p_car.check_confirmation(p_trinket)
	log('[responsed]')
	p_car.expire_challenges()
	p_trinket.expire_challenges()
	p_car.execute_command()


