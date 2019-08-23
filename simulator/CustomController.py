from time import sleep
import Constants
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
        self.errorState = LemonatorErrors.NONE

        self.inputLevel = ""
        self.targetLevel = -1
        self.startLevel = -1
        self.inputTemperature = ""
        self.targetTemperature = -1
        self.inputRatio = ""
        self.targetRatio = -1
        self.latestKeyPress = ""

        self.aLevel = Constants.storageMax
        self.bLevel = Constants.storageMax
    
    def initialize(self):
        self.lcd.clear()

        while self.keypad.pop() != '\x00': # Emptying the buffer just in case
            pass

    def update(self):
        self.updateLeds()
        self.latestKeyPress = self.keypad.pop()

        self.lcd.pushString("\x0c     LEMONATOR\n--------------------\n")
    
        if self.errorState != LemonatorErrors.NONE:
            self.state = LemonatorState.ERROR
            self.stopFlow() # Just to be sure

            self.inputLevel = ""
            self.inputTemperature = ""
            self.inputRatio = ""

            self.displayError()
        
        # if self.pumpA.isOn():
        #     if self.aLevel <= 0:
        #         self.stopFlow()
        #         self.errorState = LemonatorErrors.EMPTY_VESSEL_A
        
        # if self.pumpB.isOn():
        #     if self.bLevel <= 0:
        #         self.stopFlow()
        #         self.errorState = LemonatorErrors.EMPTY_VESSEL_B

        if self.inputTemperature != "" and self.state != LemonatorState.USER_SELECTING_HEAT or self.targetTemperature != -1:
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

        if self.latestKeyPress == 'A':
            self.state = LemonatorState.USER_SELECTING_RATIO

    def userSelectingRatio(self):
        self.checkHeckje()

        if self.latestKeyPress.isdigit():
            self.inputRatio += self.latestKeyPress
        
        if self.latestKeyPress == '*':
            if self.inputRatio == "" or not self.inputRatio.isnumeric() or float(self.inputRatio or 0) <= 0:
                self.errorState = LemonatorErrors.INVALID_INPUT
                return
            
            self.targetRatio = float(self.inputRatio)
            self.inputRatio = ""
            self.state = LemonatorState.USER_SELECTING_VOLUME

        self.lcd.pushString(f"Desired vol. ratio:\n1 to {self.inputRatio} | B to A (*)")

    def userSelectingVolume(self):
        self.checkHeckje()

        if self.latestKeyPress.isdigit():
            self.inputLevel += self.latestKeyPress
        
        if self.latestKeyPress == '*':
            if self.inputLevel == "" or not self.inputLevel.isnumeric() or float(self.inputLevel or 0) <= 0:
                self.errorState = LemonatorErrors.INVALID_INPUT
                return

            self.targetLevel = float(self.inputLevel)
            if self.targetLevel / (self.targetRatio + 1) > self.bLevel:
                self.errorState = LemonatorErrors.B_SHORTAGE
                return

            if self.targetLevel * self.targetRatio / (self.targetRatio + 1) > self.aLevel:
                self.errorState = LemonatorErrors.A_SHORTAGE
                return

            self.startLevel = self.level._convertToValue()
            if self.startLevel + self.targetLevel > Constants.liquidMax:
                self.errorState = LemonatorErrors.INVALID_INPUT
                return

            self.inputLevel = ""
            self.state = LemonatorState.USER_SELECTING_HEAT

        self.lcd.pushString(f"Desired volume:\n{self.inputLevel} mL (*)")

    def userSelectingHeat(self):
        self.checkHeckje()

        if self.latestKeyPress.isdigit():
            self.inputTemperature += self.latestKeyPress

        if self.latestKeyPress == '*':
            if self.inputTemperature == "" or not self.inputTemperature.isnumeric():
                self.errorState = LemonatorErrors.INVALID_INPUT
                return

            self.targetTemperature = float(self.inputTemperature)
            if self.targetTemperature < Constants.environmentTemp:
                self.targetTemperature = Constants.environmentTemp
            if self.targetTemperature > 90:
                self.errorState = LemonatorErrors.TEMP_TOO_HIGH
                self.targetTemperature = -1
                return
            
            self.inputTemperature = ""
            self.state = LemonatorState.DISPENSING_B
        
        self.lcd.pushString(f"Desired temperature:\n{self.inputTemperature} deg C (*)")

    def dispensingAState(self):
        self.checkHeckje()

        if not self.presence.readValue():
            self.stopFlow()
            self.errorState = LemonatorErrors.CUP_REMOVED
            return

        desiredALevel = self.startLevel + self.targetLevel
        if self.level._convertToValue() >= desiredALevel:
            self.stopFlow()
            self.aLevel -= self.targetLevel * self.targetRatio / (self.targetRatio + 1)
            self.state = LemonatorState.IDLE
            return
        
        self.dispenseA()

        self.lcd.pushString(f"Dispensing A\n{int(self.level._convertToValue())}/{int(desiredALevel)} progress")

    def dispenseA(self):
        if not self.pumpA.isOn():
            self.pumpA.switchOn()
        if self.valveA.isOn():
            self.valveA.switchOff()
        
        self.checkHeckje()

    def dispensingBState(self):
        self.checkHeckje()

        if not self.presence.readValue():
            self.stopFlow()
            self.errorState = LemonatorErrors.CUP_REMOVED
            return

        desiredBLevel = self.startLevel + self.targetLevel / (self.targetRatio + 1)
        if self.level._convertToValue() >= desiredBLevel:
            self.stopFlow()
            self.bLevel -= self.targetLevel / (self.targetRatio + 1)
            self.state = LemonatorState.DISPENSING_A
            return

        self.dispenseB()

        self.lcd.pushString(f"Dispensing B\n{int(self.level._convertToValue())}/{int(desiredBLevel)} progress")

    def dispenseB(self):
        if not self.pumpB.isOn():
            self.pumpB.switchOn()
        if self.valveB.isOn():
            self.valveB.switchOff()
        
        self.checkHeckje()

    def checkHeckje(self):
        if self.latestKeyPress == '#':
            self.state = LemonatorState.IDLE
            self.stopFlow()
            self.heater.switchOff()
            self.targetTemperature = -1

    def handleHeater(self):
        if not self.presence.readValue():
            self.heater.switchOff()
            self.targetTemperature = -1
            return
        
        if self.targetTemperature >= 0 and self.temperature._convertToValue() < self.targetTemperature:
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
        
        if self.heater.isOn():
            self.ledGreenM.switchOff()
            self.ledYellowM.switchOn()
        
        else:
            self.ledGreenM.switchOn()
            self.ledYellowM.switchOff()
    
    def displayError(self):
        self.lcd.pushString("\x0c  ERROR\n--------------------\n")

        errorMessage = ""
        if self.errorState == LemonatorErrors.NONE:
            return
        elif self.errorState == LemonatorErrors.EMPTY_VESSEL_A:
            errorMessage = "Vessel A is empty"
        elif self.errorState == LemonatorErrors.EMPTY_VESSEL_B:
            errorMessage = "Vessel B is empty"
        elif self.errorState == LemonatorErrors.INVALID_INPUT:
            errorMessage = "Input is invalid"
        elif self.errorState == LemonatorErrors.TEMP_TOO_HIGH:
            errorMessage = "Input temp too high"
        elif self.errorState == LemonatorErrors.CUP_REMOVED:
            errorMessage = "Cup was removed"
        elif self.errorState == LemonatorErrors.A_SHORTAGE:
            errorMessage = "Too little in A"
        elif self.errorState == LemonatorErrors.B_SHORTAGE:
            errorMessage = "Too little in B"

        self.lcd.pushString(f"{errorMessage}\nPress # to return")
        if self.latestKeyPress == '#':
            self.state = LemonatorState.IDLE
            self.errorState = LemonatorErrors.NONE