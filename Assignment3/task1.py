import machine
import time
led = machine.Pin(14,machine.Pin.OUT)
button = machine.Pin(32,machine.Pin.IN, machine.Pin.PULL_UP)
try:
    while True:
        if not button.value():
            led.value(True)
            time.sleep(0.5)
            led.value(False)
            time.sleep(0.5)
except:
    pass