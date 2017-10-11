from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from Simulator import Simulator
from typing import Dict
from time import sleep

class lemonator:

    def __init__(self, gui = False, ):

    class led_yellow(lemonator):

        def set(c: bool):
            if c:
                self.SimProxy__sensors["led_yellow"].switchOn()
            else:
                self.SimProxy__sensors["led_yellow"].switchOff()
