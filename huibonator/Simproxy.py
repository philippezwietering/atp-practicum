from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from Simulator import Plant
from typing import Dict
from time import sleep

class lemonator:

    def __init__(self, plant):
        self.plant = plant
        self.led_yellow = led_yellow(plant)
        self.led_green = led_green(plant)
        self.water_pump = water_pump(plant)
        self.sirup_pump = sirup_pump(plant)
        self.water_valve = water_valve(plant)
        self.sirup_valve = sirup_valve(plant)
        self.heater = heater(plant)

class output:

    def __init__(self, plant):
        self.plant = plant

class led_yellow(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["led_yellow"].switchOn()
        else:
            self.plant._effectors["led_yellow"].switchOff()

class led_green(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["led_green"].switchOn()
        else:
            self.plant._effectors["led_green"].switchOff()

#pumpa water pump

class water_pump(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["pumpA"].switchOn()
        else:
            self.plant._effectors["pumpA"].switchOff()

class sirup_pump(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["pumpB"].switchOn()
        else:
            self.plant._effectors["pumpB"].switchOff()

class water_valve(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["valveA"].switchOn()
        else:
            self.plant._effectors["ValveA"].switchOff()

class sirup_valve(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["valeB"].switchOn()
        else:
            self.plant._effectors["valveB"].switchOff()

class heater(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["heater"].switchOn()
        else:
            self.plant._effectors["heater"].switchOff()
