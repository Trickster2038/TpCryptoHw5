from car import Car
from trinket import Trinket
from logger import *

def register(p_trinket, p_car):
	p_car.set_trinket_key(p_trinket)
	p_trinket.set_car_key(p_car)
	log('register')
