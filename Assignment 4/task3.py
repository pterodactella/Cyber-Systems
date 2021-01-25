import machine
import network
import socket
import time  
import json

pinDict = {
  'led': machine.Pin(13, machine.Pin.IN),
}

sensDict = {
  'butt': machine.Pin(14, machine.Pin.IN,machine.Pin.PULL_UP),
  'temp': machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23)),
}

paths = ["/pins", "/sensors", "/pins/<pin_name>", "/sensor/<sensor_name>"]

jsonH = "HTTP/1.1 200 OK\nContent-Type: application/json\n\n"

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
address = 24
temp_reg = 5
res_reg = 8
data = i2c.readfrom_mem(address, temp_reg, 2)
data = bytearray(2)
i2c.readfrom_mem_into(address, temp_reg, data)
def temp_c(data):
    data = i2c.readfrom_mem(address, temp_reg, 2)
    value = data[0] << 8 | data[1]
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

jsons=""

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
        if path == "/":
            jsons = jsonH + json.dumps("Valid paths are:      " + "      ".join(paths))
        elif path == "/pins":
            pins = [x for x in pinDict]
            jsons = jsonH + json.dumps("Pins are:      " + "      ".join(pins))                      
        elif path == "/sensors":
            sens = [x for x in sensDict]
            jsons = jsonH + json.dumps("Pins are:      " + "      ".join(sens))    
        elif '/pins/' in path:
            if path[6:] in pinDict:
                jsons = jsonH + json.dumps(pinDict[path[6:]].value())                      
            else:
                jsons = jsonH + json.dumps("No pin with that name")
        elif '/sensor/' in path:
            if path[8:] in sensDict:
                if path[8:].lower() == "temp":
                    jsons = jsonH + json.dumps(temp_c(data))
                else:
                    jsons = jsonH + json.dumps(sensDict[path[8:]].value())                      
            else:
                jsons = jsonH + json.dumps("No sensor with that name")
    print(path)
    cl.send(jsons)
    cl.close()
