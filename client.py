# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket

s = socket.socket()

#TODO Check validity of input (?)
host = input('Enter the EV3\'s IP address: ')
port = 1234

s.connect((host, port))
print ((s.recv(1024)).decode('utf-8'))
s.close()
