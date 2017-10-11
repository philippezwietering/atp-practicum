import pygame
from pygame import *
from Constants import *
from Vessel import Vessel
from Effector import Heater
from Sensor import Sensor
from time import sleep


class GUI:
    def __init__(self, plant = None, controller = None, monitor = None):
        self.__plant = plant
        self.__controller = controller
        self.__monitor = monitor
        self.__timestamp = 0
        self.__run = False
        self.__tap = False

        # Initialise PyGame
        pygame.init()
        pygame.font.init()
        self.__font = pygame.font.Font('font/OpenSans-Regular.ttf', 12)
        # Define a screen
        self.__screen = pygame.display.set_mode((1040, 400))
        pygame.display.set_caption('Liquid Mixer Simulator GUI')
        pygame.mouse.set_visible(True)

        # Create components
        self.__icons = {}
        self.__icons["a"] = VesselIcon(self.__screen, 100, 50, self.__plant._vessels["a"])
        self.__icons["b"] = VesselIcon(self.__screen, 300, 50, self.__plant._vessels["b"])
        self.__icons["mix"] = VesselIcon(self.__screen, 200, 125, self.__plant._vessels["mix"])
        self.__icons["heater"] = HeaterIcon(self.__screen, 200, 185, self.__plant._effectors["heater"])
        self.__icons["temp"] = SensorIcon(self.__screen, 275, 125, self.__plant._sensors["temp"], "Temperature")
        self.__icons["level"] = SensorIcon(self.__screen, 275, 150, self.__plant._sensors["level"], "Level")
        self.__icons["color"] = SensorIcon(self.__screen, 275, 175, self.__plant._sensors["color"], "Colour")
        self.__icons["reflex"] = SensorIcon(self.__screen, 275, 200, self.__plant._sensors["reflex"], "Iscup?")

        # Draw
        self.step()

    def drawPipes(self) -> None:
        pygame.draw.lines(self.__screen, (0, 0, 0) if self.__plant._effectors["pumpA"].isOn() else (240,240,240), False,
                          [(135, 55), (135, 35), (215, 35), (215, 140)], 5)


        pygame.draw.lines(self.__screen, (0, 0, 0) if self.__plant._effectors["pumpB"].isOn() else (240,240,240), False,
                          [(235, 140), (235, 35), (315, 35), (315, 55)], 5)

    def drawButtons(self) -> None:
        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 10, 60, 30])
        if self.__run:
            pygame.draw.rect(self.__screen, (240, 240, 240), [517, 15, 10, 20])
            pygame.draw.rect(self.__screen, (240, 240, 240), [532, 15, 10, 20])
        else:
            pygame.draw.polygon(self.__screen, (240, 240, 240), [(527, 15), (527, 35), (543, 25)])
        pygame.draw.rect(self.__screen, (240, 120, 0), [570, 10, 60, 30])
        pygame.draw.polygon(self.__screen, (240, 240, 240), [(585, 15), (585, 35), (600, 25)])
        pygame.draw.rect(self.__screen, (240, 240, 240), [605, 15, 10, 20])

        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 50, 130, 30])
        pumpA = "Pump A: "+("on " if self.__plant._effectors["pumpA"].isOn() else "off")
        label = self.__font.render(pumpA, False, (240, 240, 240))
        self.__screen.blit(label, [530, 55])

        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 90, 130, 30])
        pumpB = "Pump B: "+("on " if self.__plant._effectors["pumpB"].isOn() else "off")
        label = self.__font.render(pumpB, False, (240, 240, 240))
        self.__screen.blit(label, [530, 95])

        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 130, 130, 30])
        heater = "Heater: "+("on " if self.__plant._effectors["heater"].isOn() else "off")
        label = self.__font.render(heater, False, (240, 240, 240))
        self.__screen.blit(label, [530, 135])

        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 170, 130, 30])
        tap = "Tap: "+("on " if self.__tap else "off")
        label = self.__font.render(tap, False, (240, 240, 240))
        self.__screen.blit(label, [530, 175])

        pygame.draw.rect(self.__screen, (240, 240, 0), [650, 10, 60, 30])
        yellowLed = "Yled: "+("on " if self.__plant._effectors["led_yellow"].isOn() else "off")
        label = self.__font.render(yellowLed, False, (0, 0, 0))
        self.__screen.blit(label, [660, 15])

        pygame.draw.rect(self.__screen, (0, 240, 0), [720, 10, 60, 30])
        greenLed = "Gled: "+("on " if self.__plant._effectors["led_green"].isOn() else "off")
        label = self.__font.render(greenLed, False, (0, 0, 0))
        self.__screen.blit(label, [730, 15])

        pygame.draw.rect(self.__screen, (240, 120, 0), [650, 50, 130, 30])
        cup = ("Remove " if self.__plant._vessels["mix"].getPresence() else "Insert ") +"Cup"
        label = self.__font.render(cup, False, (240, 240, 240))
        self.__screen.blit(label, [680, 55])

        pygame.draw.rect(self.__screen, (240, 120, 0), [650, 90, 130, 30])
        empty = "Empty cup"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [680, 95])

        #Keypad
        #row 1
        pygame.draw.rect(self.__screen, (240, 120, 0), [800, 10, 35, 30])
        empty = "1"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [815, 15])

        pygame.draw.rect(self.__screen, (240, 120, 0), [840, 10, 35, 30])
        empty = "2"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [855, 15])

        pygame.draw.rect(self.__screen, (240, 120, 0), [880, 10, 35, 30])
        empty = "3"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [895, 15])

        pygame.draw.rect(self.__screen, (240, 120, 0), [920, 10, 35, 30])
        empty = "A"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [935, 15])
        #row 2
        pygame.draw.rect(self.__screen, (240, 120, 0), [800, 45, 35, 30])
        empty = "4"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [815, 50])

        pygame.draw.rect(self.__screen, (240, 120, 0), [840, 45, 35, 30])
        empty = "5"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [855, 50])

        pygame.draw.rect(self.__screen, (240, 120, 0), [880, 45, 35, 30])
        empty = "6"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [895, 50])

        pygame.draw.rect(self.__screen, (240, 120, 0), [920, 45, 35, 30])
        empty = "B"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [935, 50])

        #row 3
        pygame.draw.rect(self.__screen, (240, 120, 0), [800, 80, 35, 30])
        empty = "7"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [815, 85])

        pygame.draw.rect(self.__screen, (240, 120, 0), [840, 80, 35, 30])
        empty = "8"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [855, 85])

        pygame.draw.rect(self.__screen, (240, 120, 0), [880, 80, 35, 30])
        empty = "9"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [895, 85])

        pygame.draw.rect(self.__screen, (240, 120, 0), [920, 80, 35, 30])
        empty = "C"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [935, 85])

        #row 4
        pygame.draw.rect(self.__screen, (240, 120, 0), [800, 115, 35, 30])
        empty = "*"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [815, 120])

        pygame.draw.rect(self.__screen, (240, 120, 0), [840, 115, 35, 30])
        empty = "0"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [855, 120])

        pygame.draw.rect(self.__screen, (240, 120, 0), [880, 115, 35, 30])
        empty = "#"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [895, 120])

        pygame.draw.rect(self.__screen, (240, 120, 0), [920, 115, 35, 30])
        empty = "D"
        label = self.__font.render(empty, False, (240, 240, 240))
        self.__screen.blit(label, [935, 120])



    def drawGraphs(self) -> None:
        scale = 140 / 3.3
        # Temperature
        pygame.draw.lines(self.__screen, (0, 0, 0), False, [(30, 240), (30, 380), (200, 380)])
        label = self.__font.render("0", False, (0, 0, 0))
        self.__screen.blit(label, [20, 380])
        label = self.__font.render("3.3", False, (0, 0, 0))
        self.__screen.blit(label, [10, 230])
        x0 = 30
        y0 = 380
        pygame.draw.line(self.__screen, (240, 120, 0), [x0, y0 - (tempSetPoint * scale)], [x0 + 170, y0 - tempSetPoint * scale])
        label = self.__font.render(str(tempSetPoint), False, (240, 120, 0))
        self.__screen.blit(label, [5, y0 - (tempSetPoint * scale) - 10])

        if len(self.__monitor._sensorReadings["temp"]) < 170:
            x, y = x0, y0
        else:
            x = x0
            y = y0 - self.__monitor._sensorReadings["temp"][-170] * scale
        for reading in self.__monitor._sensorReadings["temp"][-170:]:
            prevX, prevY = x, y
            x += 1
            y = y0 - (reading * scale)
            pygame.draw.line(self.__screen, (240, 0, 0), [prevX, prevY], [x, y], 2)
        x, y = x0, y0
        for value in self.__monitor._effectorValues["heater"][-170:]:
            x += 1
            y = y0-20 if value else y0
            pygame.draw.line(self.__screen, (120, 120, 0), [x, y0], [x, y])
        label = self.__font.render("Temperature", False, (0, 0, 0))
        self.__screen.blit(label, [80, 225])

        # Level
        pygame.draw.lines(self.__screen, (0, 0, 0), False, [(240, 240), (240, 380), (410, 380)])
        label = self.__font.render("0", False, (0, 0, 0))
        self.__screen.blit(label, [230, 380])
        label = self.__font.render("3.3", False, (0, 0, 0))
        self.__screen.blit(label, [220, 230])
        x0 = 240
        pygame.draw.line(self.__screen, (240, 120, 0), [x0, y0 - (levelSetPoint * scale)], [x0 + 170, y0 - levelSetPoint * scale])
        label = self.__font.render(str(levelSetPoint), False, (240, 120, 0))
        self.__screen.blit(label, [210, y0 - (levelSetPoint * scale) - 10])

        if len(self.__monitor._sensorReadings["level"]) < 170:
            x, y = x0, y0
        else:
            x = x0
            y = y0 - self.__monitor._sensorReadings["level"][-170] * scale
        for reading in self.__monitor._sensorReadings["level"][-170:]:
            prevX, prevY = x, y
            x += 1
            y = y0 - (reading * scale)
            pygame.draw.line(self.__screen, (0, 240, 0), [prevX, prevY], [x, y], 2)
        x, y = x0, y0
        for value1, value2 in zip(self.__monitor._effectorValues["pumpA"][-170:], self.__monitor._effectorValues["pumpB"][-170:]):
            x += 1
            y = y0-15 if value1 else y0
            pygame.draw.line(self.__screen, (120, 0, 120), [x, y0], [x, y])
            y = y0-7 if value2 else y0
            pygame.draw.line(self.__screen, (0, 120, 120), [x, y0], [x, y])
        label = self.__font.render("Level", False, (0, 0, 0))
        self.__screen.blit(label, [280, 225])

        # Colour
        pygame.draw.lines(self.__screen, (0, 0, 0), False, [(450, 240), (450, 380), (620, 380)])
        label = self.__font.render("0", False, (0, 0, 0))
        self.__screen.blit(label, [440, 380])
        label = self.__font.render("3.3", False, (0, 0, 0))
        self.__screen.blit(label, [430, 230])
        x0 = 450
        pygame.draw.line(self.__screen, (240, 120, 0), [x0, y0 - (colourSetPoint * scale)], [x0 + 170, y0 - colourSetPoint * scale])
        label = self.__font.render(str(colourSetPoint), False, (240, 120, 0))
        self.__screen.blit(label, [420, y0 - (colourSetPoint * scale) - 10])

        if len(self.__monitor._sensorReadings["color"]) < 170:
            x, y = x0, y0
        else:
            x = x0
            y = y0 - self.__monitor._sensorReadings["color"][-170] * scale
        for reading in self.__monitor._sensorReadings["color"][-170:]:
            prevX, prevY = x, y
            x += 1
            y = y0 - (reading * scale)
            pygame.draw.line(self.__screen, (0, 0, 240), [prevX, prevY], [x, y], 2)
        label = self.__font.render("Colour", False, (0, 0, 0))
        self.__screen.blit(label, [480, 225])


    def update(self) -> None:
        self.__screen.fill((250, 250, 250))
        for icon in self.__icons.values():
            icon.draw()
        self.drawPipes()

        self.drawButtons()
        self.drawGraphs()

        label = self.__font.render(str(self.__timestamp), True, (0, 0, 0))
        self.__screen.blit(label, [10, 10])

        pygame.display.update()

    def step(self) -> None:
        self.__timestamp += 1
        self.__plant.update()
        self.__controller.update()
        self.__monitor.update()
        if self.__tap:
            self.__plant._vessels["mix"].flow()

    def run(self) -> None:
        while True:
            if self.__run:
                self.step()

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 500 < pos[0] <= 630:
                        if 10 < pos[1] <= 40 and pos[0] < 560:
                            self.__run = False if self.__run else True
                        elif 10 < pos[1] <= 40 and pos[0] > 560:
                            if not self.__run:
                                self.step()
                        elif 50 < pos[1] <= 80:
                            self.__plant._effectors["pumpA"].switchOff() if self.__plant._effectors["pumpA"].isOn() else self.__plant._effectors["pumpA"].switchOn()
                        elif 90 < pos[1] <= 120:
                            self.__plant._effectors["pumpB"].switchOff() if self.__plant._effectors["pumpB"].isOn() else self.__plant._effectors["pumpB"].switchOn()
                        elif 130 < pos[1] <= 160:
                            self.__plant._effectors["heater"].switchOff() if self.__plant._effectors["heater"].isOn() else self.__plant._effectors["heater"].switchOn()
                        elif 170 < pos[1] <= 200:
                            self.__tap = False if self.__tap else True
                    elif 650 < pos[0] < 780:
                        if 10 < pos[1] <= 40 and pos[0] < 710:
                            self.__plant._effectors['led_yellow'].toggle()
                        elif 10 < pos[1] <= 40 and pos[0] > 710:
                            self.__plant._effectors['led_green'].toggle()
                        elif 50 < pos[1] <= 80:
                            self.__plant._vessels["mix"].toggle()
                        elif 90 < pos[1] <= 120:
                            self.__plant._vessels["mix"].empty()
                    #keypad
                    elif 800 < pos[0] <= 835:
                        if 10 < pos[1] <= 40:
                            self.__plant._sensors["keypad"].pressKey('1')
                        elif 45 < pos[1] <= 75:
                            self.__plant._sensors["keypad"].pressKey('4')
                        elif 80 < pos[1] <= 115:
                            self.__plant._sensors["keypad"].pressKey('7')
                        elif 120 < pos[1] <= 155:
                            self.__plant._sensors["keypad"].pressKey('*')
                    elif 840 < pos[0] <= 885:
                        if 10 < pos[1] <= 40:
                            self.__plant._sensors["keypad"].pressKey('2')
                        elif 45 < pos[1] <= 75:
                            self.__plant._sensors["keypad"].pressKey('5')
                        elif 80 < pos[1] <= 115:
                            self.__plant._sensors["keypad"].pressKey('8')
                        elif 120 < pos[1] <= 155:
                            self.__plant._sensors["keypad"].pressKey('0')
                    elif 890 < pos[0] <= 925:
                        if 10 < pos[1] <= 40:
                            self.__plant._sensors["keypad"].pressKey('3')
                        elif 45 < pos[1] <= 75:
                            self.__plant._sensors["keypad"].pressKey('6')
                        elif 80 < pos[1] <= 115:
                            self.__plant._sensors["keypad"].pressKey('9')
                        elif 120 < pos[1] <= 155:
                            self.__plant._sensors["keypad"].pressKey('#')
                    elif 930 < pos[0] <= 965:
                        if 10 < pos[1] <= 40:
                            self.__plant._sensors["keypad"].pressKey('A')
                        elif 45 < pos[1] <= 75:
                            self.__plant._sensors["keypad"].pressKey('B')
                        elif 80 < pos[1] <= 115:
                            self.__plant._sensors["keypad"].pressKey('C')
                        elif 120 < pos[1] <= 155:
                            self.__plant._sensors["keypad"].pressKey('D')

            self.update()
            sleep(0.25)


class Icon:
    def __init__(self, screen: pygame.display, x: int = 0, y: int = 0):
        self._x = x
        self._y = y
        self._screen = screen
        self._font = pygame.font.Font('font/OpenSans-Regular.ttf', 12)

    def draw(self) -> None:
        text = self._font.render("?", False, (0,0,0))
        self._screen.blit(text, [self._x, self._y])


class VesselIcon(Icon):
    def __init__(self, screen: pygame.display, x: int, y: int, vessel: Vessel) -> None:
        Icon.__init__(self, screen, x, y)
        self._vessel = vessel

    def draw(self) -> None:
        color = self._vessel.getColour()
        level = self._vessel.getFluidAmount() / liquidMax * 100

        pygame.draw.rect(self._screen, (color*2.55, 0, 255-color*2.55), [self._x, self._y+51-(level*0.4), 50, level*0.4])
        pygame.draw.lines(self._screen, (0, 0, 0), False, [(self._x, self._y), (self._x, self._y+50), (self._x+50, self._y+50), (self._x+50, self._y)],2)


class HeaterIcon(Icon):
    def __init__(self, screen: pygame.display, x: int, y: int, heater: Heater) -> None:
        Icon.__init__(self, screen, x, y)
        self._heater = heater

    def draw(self) -> None:
        pygame.draw.line(self._screen, (0, 0, 0), [self._x, self._y], [self._x+50, self._y], 4)
        if self._heater.isOn():
            x = self._x + 2
            for i in range(6):
                pygame.draw.lines(self._screen, (0,0,0), True, [(x, self._y-2), (x+3, self._y-6), (x+6, self._y-2)], 2)
                x += 8


class SensorIcon(Icon):
    def __init__(self, screen: pygame.display, x: int, y: int, sensor: Sensor, name: str) -> None:
        Icon.__init__(self, screen, x, y)
        self._name = name
        self._sensor = sensor

    def draw(self) -> None:
        name = self._name + ":"
        value = str(self._sensor.readValue()) + " / " + self._sensor.measure()
        nameLabel = self._font.render(name, False, (0,0,0))
        self._screen.blit(nameLabel, [self._x, self._y])
        valueLabel = self._font.render(value, False, (0,0,0))
        self._screen.blit(valueLabel, [self._x+85, self._y])
