import ../huibonator/Simproxy
from time import sleep

class controller:
    def __init__(self, lemonator):
        self.lemonator = lemonator
        sleep(5)
        for x in "Hello\n":
            self.lemonator.lcd.putc(x)

    def update(self):
        if ("A" == self.lemonator.keypad.getc()) and (self.lemonator.reflex.get()):
            self.lemonator.sirup_valve.set(0)
            self.lemonator.sirup_pump.set(1)
            for x in "Pumping syrup\n":
                self.self.lemonator.lcd.putc(x)

        if self.lemonator.distance.read_mm() < 110 or not self.lemonator.reflex.get():
            self.lemonator.sirup_pump.set(0)
            self.lemonator.sirup_valve.set(1)

        self.lemonator.water_valve.set(0)
        self.lemonator.water_pump.set(1)
        for x in "Pumping water\n":
            self.lemonator.lcd.putc(x)

        if self.lemonator.distance.read_mm() < 90 or not self.lemonator.reflex.get():
            self.lemonator.water_pump.set(0)
            self.lemonator.water_valve.set(1)

        for x in "Finished!\n":
            self.lemonator.lcd.putc(x)
