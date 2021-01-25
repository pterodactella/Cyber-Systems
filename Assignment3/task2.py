import machine
import time
green = machine.Pin(14,machine.Pin.OUT)
red = machine.Pin(32, machine.Pin.OUT)
yellow = machine.Pin(15, machine.Pin.OUT)
button = machine.Pin(33,machine.Pin.IN, machine.Pin.PULL_UP)
a=0
while True:
    if a==0:
        green.value(1)
        while not button.value() :
            time.sleep(0.5)
            green.value(0)
            yellow.value(1)
            a=1
    if a==1:
        while not button.value():
            time.sleep(0.5)
            yellow.value(0)
            red.value(1)
            a=2
    if a==2:
        while not button.value():
            time.sleep(0.5)
            red.value(0)
            green.value(1)
            a=0