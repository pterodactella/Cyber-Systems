import machine
import neopixel
import time 
temp = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
address=24
temp_reg = 5
res_reg = 8
data = temp.readfrom_mem(address,temp_reg,2)
data = bytearray(2)
np1 = neopixel.NeoPixel(machine.Pin(12), 3)
temp.readfrom_mem(address,temp_reg,2)
temp.readfrom_mem_into(address,temp_reg,data)
def temp_c(data):
    value=data[0] << 8 | data[1]
    temp=(value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp
while True:
    data = temp.readfrom_mem(address,temp_reg,2)
    if temp_c(data)<=26:
        np1[0] = (255, 0, 0)
        np1[1] = (0, 0, 0)
        np1[2] = (0, 0, 0)
    	np1.write()
    elif 26<temp_c(data)<=28:
        np1[0] = (0, 0, 0)
        np1[1] = (119, 255, 0)
        np1[2] = (0, 0, 0)
	   np1.write()
    elif 28<temp_c(data):
        np1[0] = (0, 0, 0)
        np1[1] = (0, 0, 0)
        np1[2] = (0, 255,0)
   	    np1.write()
    temp_c(data)