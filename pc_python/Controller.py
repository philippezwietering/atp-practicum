import ../huibonator/Simproxy
from time import sleep

class Controller:
    def __init__(self, lemonator):
        self.lemonator = lemonator
        self.state = "Waiting"
        sleep(5)
        for x in "Hello\n":
            self.lemonator.lcd.putc(x)

    def update(self):
        if self.state == "Waiting":
            if ("A" == self.lemonator.keypad.getc()) and (self.lemonator.reflex.get()):
                self.state = "Pumping sirup"
                self.lemonator.sirup_pump.set(1)
                self.lemonator.sirup_valve.set(0)
                for x in "Pumping sirup\n":
                    self.lemonator.lcd.putc(x)

        if self.state == "Pumping sirup":
            if not self.lemonator.reflex.get():
                self.lemonator.sirup_valve.set(1)
                self.lemonator.sirup_pump.set(0)
                self.state = "Waiting"
                for x in "Waiting\n":
                    self.lemonator.lcd.putc(x)

            if self.lemonator.distance.read_mm() < 80:
                self.lemonator.sirup_valve.set(1)
                self.lemonator.sirup_pump.set(0)
                self.state = "Pumping water"
                self.lemonator.water_pump.set(1)
                self.lemonator.water_valve.set(0)
                for x in "Pumping water\n":
                    self.lemonator.lcd.putc(x)


        if self.state == "Pumping water":
            if not self.lemonator.reflex.get() or self.lemonator.distance.read_mm() < 45:
                self.lemonator.water_pump.set(0)
                self.lemonator.water_valve.set(1)
                self.state = "Waiting"
                for x in "Waiting\n":
                    self.lemonator.lcd.putc(x)
