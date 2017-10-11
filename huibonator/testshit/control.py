import proxy

class controller:

    def update(self):
        hw = self.interface
        led = hw._led_yellow

        led.set(1)

a = proxy.proxy(controller())
a.run()
