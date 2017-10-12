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


class led_yellow:

    def __init__(self, plant):
        self.plant = plant

    def set(self, c: bool):
        if c:
            self.plant._effectors["led_yellow"].switchOn()
        else:
            self.plant._effectors["led_yellow"].switchOff()
