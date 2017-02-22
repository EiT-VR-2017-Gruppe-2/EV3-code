#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time
import socket

print('Hello World!')
s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host, port))

s.listen(5)

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(('trololo').encode('utf-8'))
    c.close()