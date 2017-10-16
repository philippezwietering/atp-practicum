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
        self.colour = colour(plant)
        self.distance = distance(plant)
        self.reflex = reflex(plant)
        self.lcd = lcd(plant)
        self.keypad = keypad(plant)

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
            self.plant._effectors["valveA"].switchOff()

class sirup_valve(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["valveB"].switchOn()
        else:
            self.plant._effectors["valveB"].switchOff()

class heater(output):

    def set(self, c: bool):
        if c:
            self.plant._effectors["heater"].switchOn()
        else:
            self.plant._effectors["heater"].switchOff()

class lcd(output):

    def putc(self, char):
        self.plant._effectors["LCD"].put(char)

class sensor:

    def __init__(self, plant):
        self.plant = plant

    def read_mc(self):
        pass

    def read_mm(self):
        pass

    def read_rgb(self):
        pass

    def getc(self):
        pass

    def get(self):
        pass

class colour(sensor):

    def read_rgb(self):
        print("unimplemented")

class distance(sensor):

    def read_mm(self):

        def magicalconversion(OldValue, OldMin, OldMax, NewMin, NewMax):
            return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

        return int(magicalconversion(self.plant._sensors["level"]._convertToValue(), 0, 2000, 88, 44))

class reflex(sensor):

    def get(self):
        return int(self.plant._sensors["reflex"].readValue())

class keypad(sensor):

    def getc(self):
        return(self.plant._sensors["keypad"]).getc()
