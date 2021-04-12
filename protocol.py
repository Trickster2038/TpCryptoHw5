from logger import *

'''
This class implements 3-step 'handshake' protocol
    [0 - registering car-trinket pair (exchange of public keys)]
	1 - trinket -> car (command, challenge_for_Car)
	2 - car -> trinket (confirmation_from_Car, challenge_for_Trinket)
	3 - trinket -> car (confirmation_from_Trinket)
	[4 - executing command on car-side and expiring challenge]
'''

def register(p_trinket, p_car):
	p_car.set_side_pubkey(p_trinket)
	p_trinket.set_side_pubkey(p_car)
	
	# 0: (registration) 0xXXXXXXXXXXXX (pubkey1 written to trinked), 0xXXXXXXXXXXXXXX (pubkey2 written to car)
	print('\n0: (registration) \n{} <...> (pubkey1 written to trinket), \n{} <...> (pubkey2 written to car)'
		.format(p_car.get_pubkey().save_pkcs1()[32:70].decode(), 
			p_trinket.get_pubkey().save_pkcs1()[32:70].decode()))
	

def handshake(p_trinket, p_car):
	p_car.set_outer_challenge(p_trinket)
	p_car.set_command(p_trinket.get_command())

	#1: (handshake) trinket -> car, 0xXXXXXX (id command), 0xXXXXXXX (challenge for car)
	print('1: (handshake) {} -> {}, {} (id command), {} (challenge for car)'
		.format(p_trinket.name, p_car.name, p_car.command, p_car.outer_challenge.get_text().decode()[0:20]))
	

def challenge(p_trinket, p_car):
	p_trinket.set_outer_challenge(p_car)
	p_trinket.check_confirmation(p_car)

	#2: (challenge) car -> trinket: 0xXXXXXX(challenge for trinket), 0xXXXXXXX (confirm challenge for car)
	print('2: (challenge) {} -> {}, {} (challenge for trinket), {} (confirm challenge for car)'
		.format(p_car.name, p_trinket.name, p_trinket.outer_challenge.get_text().decode()[0:8], 
			p_car.signature.hex()[0:8]))

def response(p_trinket, p_car):
	p_car.check_confirmation(p_trinket)

	#3: (response) trinket->car: 0xXXXXXXX (confirm challenge for trinket)
	print('3: (response) {} -> {}, {} (confirm challenge for trinket)'
		.format(p_trinket.name, p_car.name, p_trinket.signature.hex()[0:20]))

	''' 
	if 'handshake' is succesful - car executes command 
	else - exception was thrown and will be cathed in main program
	'''
	p_car.execute_command()

	# challenges expires to avoid re-use of command
	p_car.expire_challenges()
	p_trinket.expire_challenges()
	