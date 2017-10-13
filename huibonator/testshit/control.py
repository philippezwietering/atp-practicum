from sim import Plant, Simulator
import proxy

myplant = Plant()
lemonator = proxy.proxy(myplant)
led = lemonator.led_yellow


class controller:

    def update(self):

        led.set(1)
        delay(1000)
        led.set(0)


sim = Simulator(True, myplant, controller())

sim.run()
