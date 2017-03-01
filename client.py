# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket

# Validate if input has the structure of an IPv4-address
def validateIPv4(input):
    split = input.split('.')
    if len(split) != 4:
        return False
    for x in split:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0  or i > 255:
            return False
    return True

s = socket.socket()

#TODO Check validity of input (?)
while True:
    host = input("Enter the EV3\'s IP address: ")       # TODO: Check if raw_input works for the EV3
    if not validateIPv4(host):
        print("Invalid IPv4-address, please try again.")
    else:
        break

port = 1234

s.connect((host, port))
print ((s.recv(1024)).decode('utf-8'))
while True:
    msg = input('Enter a command: ')
    if msg == '':
        break
    s.send(msg.encode('utf-8'))
s.close()
