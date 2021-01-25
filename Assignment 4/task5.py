import machine
import network
import socket
import time  
import json
import neopixel

pinDict = {
  'led': machine.Pin(32, machine.Pin.OUT),
  'np': 0,
}

sensDict = {
  'butt': machine.Pin(14, machine.Pin.IN,machine.Pin.PULL_UP),
  'temp': machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23)),
  'potent': machine.ADC(machine.Pin(34))
}

paths = ["/pins", "/sensors", "/pins/<pin_name>", "/sensor/<sensor_name>"]

jsonH = "HTTP/1.1 200 OK\nContent-Type: application/json\n\n"

led2 = machine.PWM(machine.Pin(13),5000)
pot = machine.ADC(machine.Pin(34))
pot.width(machine.ADC.WIDTH_10BIT)
pot.atten(machine.ADC.ATTN_11DB)
np = neopixel.NeoPixel(machine.Pin(12), 2)
np[0] = (0, 0, 0)
np[1] = (0, 0, 0)
np.write()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
address = 24
temp_reg = 5
res_reg = 8
data = i2c.readfrom_mem(address, temp_reg, 2)
data = bytearray(2)
i2c.readfrom_mem_into(address, temp_reg, data)
def temp_c(data):
    data = i2c.readfrom_mem(address, temp_reg, 2)
    value = data[0] << 8 or data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'esp32')
ap.config (authmode = 3, password = '12345678')

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

jsons = jsons = jsonH + json.dumps("Valid paths are:      " + "      ".join(paths))

while True:
    data = i2c.readfrom_mem(address,temp_reg,2)
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        decoded = line.decode()
        if "GET" in decoded:
            path = decoded.split(" ")[1]
        if not line or line == b'\r\n':
            break
        if path == "/pins" or path == "/pins/":
            pins = [x for x in pinDict]
            jsons = jsonH + json.dumps("Pins are:      " + "      ".join(pins))                      
        elif path == "/sensors" or path == "/sensors/":
            sens = [x for x in sensDict]
            jsons = jsonH + json.dumps("Sensors are:      " + "      ".join(sens))    
        elif '/pins/' in path:
            if path == "/pins/led/on" or path == "/pins/led/on/":
                pinDict["led"].value(1)
                jsons = jsonH + json.dumps("LED now on")

            elif path == "/pins/led/off" or path == "/pins/led/off/":
                pinDict["led"].value(0)
                jsons = jsonH + json.dumps("LED now off")

            elif path == "/pins/np/1/red" or path == "/pins/np/1/red/":
                np[0] = (0, 255, 0)
                np.write()
                jsons = jsonH + json.dumps("First neopixel now red")

            elif path == "/pins/np/1/green" or path == "/pins/np/1/green/":
                np[0] = (255, 0, 0)
                np.write()
                jsons = jsonH + json.dumps("First neopixel now green") 

            elif path == "/pins/np/1/blue" or path == "/pins/np/1/blue/":
                np[0] = (0, 0, 255)
                np.write()
                jsons = jsonH + json.dumps("First neopixel now blue")

            elif path == "/pins/np/2/red" or path == "/pins/np/2/red/":
                np[1] = (0, 255, 0)
                np.write()
                jsons = jsonH + json.dumps("Second neopixel now red")

            elif path == "/pins/np/2/green" or path == "/pins/np/2/green/":
                np[1] = (255, 0, 0)
                np.write()
                jsons = jsonH + json.dumps("Second neopixel now green") 

            elif path == "/pins/np/2/blue" or path == "/pins/np/2/blue/":
                np[1] = (0, 0, 255)
                np.write()
                jsons = jsonH + json.dumps("Second neopixel now blue")

            elif path == "/pins/np/off" or path == "/pins/np/off/":
                np[0] = (0, 0, 0)
                np[1] = (0, 0, 0)
                np.write()
                jsons = jsonH + json.dumps("Both neopixels are now off")

            elif path[6:] in pinDict:
                if path == "/pins/np":
                    jsons = jsonH + json.dumps("First NP: " + str(np[0]) + "            Second NP: " + str(np[1]))
                else:
                    jsons = jsonH + json.dumps(pinDict[path[6:]].value())                       
            else:
                jsons = jsonH + json.dumps("No pin with that name")

        elif '/sensor/' in path:
            if path[8:] in sensDict:
                if path[8:].lower() == "temp":
                    jsons = jsonH + json.dumps(temp_c(data))
                elif path[8:].lower() == "potent":
                    jsons = jsonH + json.dumps(pot.read())
                    led2.duty(pot.read())
                else:
                    jsons = jsonH + json.dumps(sensDict[path[8:]].value())                      
            else:
                jsons = jsonH + json.dumps("No sensor with that name")
    cl.send(jsons)
    cl.close()