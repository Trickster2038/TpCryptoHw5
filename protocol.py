from logger import *

def register(p_trinket, p_car):
	p_car.set_side_pubkey(p_trinket)
	p_trinket.set_side_pubkey(p_car)
	
	print('\n\n0: (registration) \n{} <...> (pubkey1 written to trinket), \n{} <...> (pubkey2 written to car)'
		.format(p_car.get_pubkey().save_pkcs1()[32:70].decode(), 
			p_trinket.get_pubkey().save_pkcs1()[32:70].decode()))
	# 0: (registration) 0xXXXXXXXXXXXX (pubkey1 written to trinked), 0xXXXXXXXXXXXXXX (pubkey2 written to car)

def handshake(p_trinket, p_car):
	p_car.set_outer_challenge(p_trinket)
	p_car.set_command(p_trinket.get_command())

	print('\n1: (handshake) {} -> {}, {} (id command), {} (challenge for car)'
		.format(p_trinket.name, p_car.name, p_car.command, p_car.outer_challenge.get_text().decode()[0:20]))
	#1: (handshake) trinket -> car, 0xXXXXXX (id command), 0xXXXXXXX (challenge for car)

def challenge(p_trinket, p_car):
	p_trinket.set_outer_challenge(p_car)
	p_trinket.check_confirmation(p_car)

	print('\n2: (challenge) {} -> {}, {} (challenge for trinket), {} (confirm challenge for car)'
		.format(p_car.name, p_trinket.name, p_trinket.outer_challenge.get_text().decode()[0:8], 
			p_car.signature.hex()[0:8]))
	#2: (challenge) car -> trinket: 0xXXXXXX(challenge for trinket), 0xXXXXXXX (confirm challenge for car)

def response(p_trinket, p_car):
	p_car.check_confirmation(p_trinket)

	print('\n3: (response) {} -> {}, {} (confirm challenge for trinket)'
		.format(p_trinket.name, p_car.name, p_trinket.signature.hex()[0:20]))
	#3: (response) trinket->car: 0xXXXXXXX (confirm challenge for trinket)

	p_car.execute_command()
	p_car.expire_challenges()
	p_trinket.expire_challenges()
	