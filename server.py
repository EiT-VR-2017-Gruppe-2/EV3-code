#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import ev3dev.fonts as fonts
import time
import socket

s = socket.socket()
host = socket.gethostname()
print('EV3 IP address:', socket.gethostbyname(host))
port = 1234
s.bind((host, port))

s.listen(5)

m = ev3.MediumMotor('outA')
#m.run_timed(time_sp=3000, speed_sp=500)


while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(('trololo').encode('utf-8'))
    while True:
        msg = (c.recv(1024)).decode('utf-8')
        if msg == '':
            break
        elif msg == 'open':
            m.run_timed(time_sp=3000, speed_sp=-500)
        elif msg == 'close':
            m.run_timed(time_sp=3000, speed_sp=500)
        else:
            ev3.Sound.speak(msg).wait()
    c.close()


