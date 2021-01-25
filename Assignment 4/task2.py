import machine
import network
import socket

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'rugbrod')
ap.config (authmode = 3, password = 'password404')

pins = machine.Pin(14, machine.Pin.IN,machine.Pin.PULL_UP)
temp = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(23))
address=24
temp_reg = 5
res_reg = 8
data = temp.readfrom_mem(address,temp_reg,2)
data = bytearray(2)
temp.readfrom_mem(address,temp_reg,2)
temp.readfrom_mem_into(address,temp_reg,data)
def temp_c(data):
    value=data[0] << 8 | data[1]
    temp=(value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    data = temp.readfrom_mem(address,temp_reg,2)
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        #print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(pins), pins.value()),'<tr><td>%s</td><td>%d</td></tr>' % ('Temp Sensor  ', temp_c(data))]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()