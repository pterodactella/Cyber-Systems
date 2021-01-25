import machine
import time 
temp = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
address=24
temp_reg = 5
res_reg = 8
data = temp.readfrom_mem(address,temp_reg,2)
data = bytearray(2)
red = machine.Pin(33, machine.Pin.OUT)
green = machine.Pin(14, machine.Pin.OUT)
orange = machine.Pin(32, machine.Pin.OUT)
temp.readfrom_mem(address,temp_reg,2)
temp.readfrom_mem_into(address,temp_reg,data)
red.value(0)
green.value(0)
orange.value(0)
def temp_c(data):
    value=data[0] << 8 | data[1]
    temp=(value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp
while True:
    data = temp.readfrom_mem(address,temp_reg,2)
    if temp_c(data)<=26:
        red.value(0)
        green.value(1)
        orange.value(0)
    elif 26<temp_c(data)<=28:
        red.value(0)
        green.value(0)
        orange.value(1)
    elif 28<temp_c(data):
        red.value(1)
        green.value(0)
        orange.value(0)
    temp_c(data)  