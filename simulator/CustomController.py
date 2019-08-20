from time import sleep
from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor, KeyPad
import Constants
from typing import Dict
from enum import Enum, auto

class LemonatorState(Enum):
    IDLE = auto()
    ERROR = auto()
    DISPENSING_A = auto()
    DISPENSING_B = auto()
    #DISPENSING_FINISHED = auto()
    USER_SELECTING_HEAT = auto()
    USER_SELECTING_VOLUME = auto()
    USER_SELECTING_RATIO = auto()

class LemonatorErrors(Enum):
    NONE = auto()
    INVALID_INPUT = auto()
    TEMP_TOO_HIGH = auto()
    EMPTY_VESSEL_A = auto()
    EMPTY_VESSEL_B = auto()
    CUP_REMOVED = auto()
    A_SHORTAGE = auto()
    B_SHORTAGE = auto()

class Controller:
    def __init__(self, pumpA, pumpB, valveA, valveB, ledRedA, ledGreenA, ledRedB, ledGreenB, ledGreenM, ledYellowM, 
                 heater, temperature, level, presence, colour, keypad, lcd):
        
        self.pumpA = pumpA
        self.pumpB = pumpB
        self.valveA = valveA
        self.valveB = valveB

        self.ledRedA = ledRedA
        self.ledGreenA = ledGreenA
        self.ledRedB = ledRedB
        self.ledGreenB = ledGreenB
        self.ledGreenM = ledGreenM
        self.ledYellowM = ledYellowM

        self.heater = heater
        self.temperature = temperature
        self.level = level
        self.presence = presence
        self.colour = colour

        self.keypad = keypad
        self.lcd = lcd

        self.state = LemonatorState.IDLE
        self.error = LemonatorErrors.NONE

        self.targetLevel = ""
        self.targetTemperature = ""
        self.heaterTemperature = None
        self.targetRatio = ""
        self.latestKeyPress = None
        
        self.cupLevel = 0
        self.aLevel = Constants.storageMax
        self.bLevel = Constants.storageMax
    
    def initialize(self):
        self.lcd.clear()

        self.cupLevel = self.level.readValue()

        while self.keypad.pop() != '\x00': # Emptying the buffer just in case
            pass

    def update(self):
        self.updateLeds()
        self.latestKeyPress = self.keypad.pop()

        self.lcd.pushString("\x0c     LEMONATOR\n--------------------\n")
    
        if self.error != LemonatorErrors.NONE:
            self.state = LemonatorState.ERROR
            self.stopFlow() # Just to be sure

            self.targetLevel = ""
            self.targetTemperature = ""
            self.targetRatio = ""

            self.displayError()
        
        if self.pumpA.isOn():
            if self.aLevel <= 0:
                self.stopFlow()
                self.error = LemonatorErrors.EMPTY_VESSEL_A
        
        if self.pumpB.isOn():
            if self.bLevel <= 0:
                self.stopFlow()
                self.error = LemonatorErrors.EMPTY_VESSEL_B

        if self.targetTemperature != "" and self.state != LemonatorState.USER_SELECTING_HEAT or self.heaterTemperature:
            self.handleHeater()

        # State switch, Python doesn't have a built-in option for this
        if self.state == LemonatorState.IDLE:
            self.idle()
        elif self.state == LemonatorState.USER_SELECTING_RATIO:
            self.userSelectingRatio()
        elif self.state == LemonatorState.USER_SELECTING_VOLUME:
            self.userSelectingVolume()
        elif self.state == LemonatorState.USER_SELECTING_HEAT:
            self.userSelectingHeat()
        elif self.state == LemonatorState.DISPENSING_A:
            self.dispensingAState()
        elif self.state == LemonatorState.DISPENSING_B:
            self.dispensingBState()
        
    def idle(self):
        self.checkHeckje()
        self.lcd.pushString("Press A to start\nPress # to cancel")

        if type(self.targetLevel) != str:
            self.targetLevel  = str(self.targetLevel)
        if type(self.targetTemperature) != str:
            self.targetTemperature = str(self.targetTemperature)

        if self.latestKeyPress == 'A':
            self.state = LemonatorState.USER_SELECTING_RATIO

    def userSelectingRatio(self):
        self.checkHeckje()

        if self.latestKeyPress.isdigit():
            self.targetRatio += self.latestKeyPress
        
        if self.latestKeyPress == '*':
            if self.targetRatio == "" or not self.targetRatio.isnumeric() or float(self.targetRatio or 0) <= 0:
                self.error = LemonatorErrors.INVALID_INPUT
                return
            
            self.targetRatio = float(self.targetRatio)
            self.state = LemonatorState.USER_SELECTING_VOLUME

        self.lcd.pushString(f"Desired vol. ratio:\n1 to {self.targetRatio} | B to A (*)")

    def userSelectingVolume(self):
        self.checkHeckje()

        if self.latestKeyPress.isdigit():
            self.targetLevel += self.latestKeyPress
        
        if self.latestKeyPress == '*':
            if self.targetLevel == "" or not self.targetLevel.isnumeric() or float(self.targetLevel or 0) <= 0:
                self.error = LemonatorErrors.INVALID_INPUT
                return

            self.targetLevel = float(self.targetLevel)
            if self.targetLevel / (self.targetRatio + 1) > self.bLevel:
                self.error = LemonatorErrors.B_SHORTAGE
                return

            if self.targetLevel * self.targetRatio / (self.targetRatio + 1) > self.aLevel:
                self.error = LemonatorErrors.A_SHORTAGE
                return

            self.startLevel = self.level._convertToValue()
            if self.startLevel + self.targetLevel > Constants.storageMax:
                self.error = LemonatorErrors.INVALID_INPUT
                return

            self.state = LemonatorState.USER_SELECTING_HEAT

        self.lcd.pushString(f"Desired volume:\n{self.targetLevel} ml (*)")

    def userSelectingHeat(self):
        self.checkHeckje()

        if self.latestKeyPress.isdigit():
            self.targetTemperature += self.latestKeyPress

        if self.latestKeyPress == '*':
            if self.targetTemperature == "" or not self.targetTemperature.isnumeric():
                self.error = LemonatorErrors.INVALID_INPUT
                return

            self.targetTemperature = float(self.targetTemperature)
            if self.targetTemperature < Constants.environmentTemp:
                self.targetTemperature = Constants.environmentTemp
            if self.targetTemperature > 90:
                self.error = LemonatorErrors.TEMP_TOO_HIGH
                return
            
            self.targetTemperature = float(self.targetTemperature)
            self.state = LemonatorState.DISPENSING_B
        
        self.lcd.pushString(f"Desired temperature:\n{self.targetTemperature} °C (*)")

    def dispensingAState(self):
        self.checkHeckje()

        if not self.presence.readValue():
            self.stopFlow()
            self.error = LemonatorErrors.CUP_REMOVED
            return
        
        self.dispenseA()

        desiredALevel = self.startLevel + self.targetLevel
        if self.level._convertToValue() >= desiredALevel:
            self.stopFlow()
            self.aLevel -= self.targetLevel * self.targetRatio / (self.targetRatio + 1)
            self.state = LemonatorState.IDLE
            self.targetLevel = ""
            self.heaterTemperature = self.targetTemperature
            self.targetTemperature = ""
            self.targetRatio = ""
        
        self.lcd.pushString(f"Dispensing A\n{round(self.level._convertToValue(), 0)}/{round(desiredALevel, 0)} progress")

    def dispenseA(self):
        if not self.pumpA.isOn():
            self.pumpA.switchOn()
        if self.valveA.isOn():
            self.valveA.isOn()

    def dispensingBState(self):
        self.checkHeckje()

        if not self.presence.readValue():
            self.stopFlow()
            self.error = LemonatorErrors.CUP_REMOVED
            return
        
        self.dispenseB()

        desiredBLevel = self.startLevel + self.targetLevel / (self.targetRatio + 1)
        if self.level._convertToValue() >= desiredBLevel:
            self.stopFlow()
            self.bLevel -= self.targetLevel / (self.targetRatio + 1)
            self.state = LemonatorState.DISPENSING_A

        self.lcd.pushString(f"Dispensing B\n{round(self.level._convertToValue(), 0)}/{round(desiredBLevel, 0)} progress")

    def dispenseB(self):
        if not self.pumpB.isOn():
            self.pumpB.switchOn()
        if self.valveB.isOn():
            self.valveB.isOn()

    def checkHeckje(self):
        if self.latestKeyPress == '#':
            self.state = LemonatorState.IDLE
            self.stopFlow()
            self.heater.switchOff()
            self.heaterTemperature = None
            return

    def handleHeater(self):
        if not self.presence.readValue():
            self.heater.switchOff()
            return
        
        target = self.targetTemperature
        if self.targetTemperature == "" and self.heaterTemperature:
            target = self.heaterTemperature
        if self.temperature._convertToValue() < target:
                self.heater.switchOn()
        else:
            self.heater.switchOff()

    def stopFlow(self):
        # This way it always stops, even when somehow the pumps were already shut down but pressure still on the vessel
        self.valveA.switchOn()
        self.valveB.switchOn()

        if self.pumpA.isOn():
            self.pumpA.switchOff()
        if self.pumpB.isOn():
            self.pumpB.switchOff()

    def updateLeds(self):
        if self.pumpA.isOn() and not self.valveA.isOn():
            self.ledGreenA.switchOn()
            self.ledRedA.switchOff()
        else:
            self.ledGreenA.switchOff()
            self.ledRedA.switchOn()
        
        if self.pumpB.isOn() and not self.valveB.isOn():
            self.ledGreenB.switchOn()
            self.ledRedB.switchOff()
        else:
            self.ledGreenB.switchOff()
            self.ledRedB.switchOn()
        
        if self.pumpA.isOn() and not self.valveA.isOn() and self.pumpB.isOn() and not self.valveB.isOn() and self.presence.readValue():
            self.ledGreenM.switchOff()
            self.ledYellowM.switchOn()
        
        else:
            self.ledGreenM.switchOn()
            self.ledYellowM.switchOff()
    
    def displayError(self):
        self.lcd.pushString("\x0c  ERROR\n--------------------\n")

        errorMessage = ""
        if self.error == LemonatorErrors.NONE:
            return
        elif self.error == LemonatorErrors.EMPTY_VESSEL_A:
            errorMessage = "Vessel A is empty"
        elif self.error == LemonatorErrors.EMPTY_VESSEL_B:
            errorMessage = "Vessel B is empty"
        elif self.error == LemonatorErrors.INVALID_INPUT:
            errorMessage = "Input is invalid"
        elif self.error == LemonatorErrors.TEMP_TOO_HIGH:
            errorMessage = "Input temp too high"
        elif self.error == LemonatorErrors.CUP_REMOVED:
            errorMessage = "Cup was removed"
        elif self.error == LemonatorErrors.A_SHORTAGE:
            errorMessage = "Too little in A"
        elif self.error == LemonatorErrors.B_SHORTAGE:
            errorMessage = "Too little in B"

        self.lcd.pushString(f"{errorMessage}\nPress # to return")
        if self.latestKeyPress == '#':
            self.state = LemonatorState.IDLE
            self.error = LemonatorErrors.NONE