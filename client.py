# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket
import pygame

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

while True:
    host = input("Enter the EV3\'s IP address: ")       # TODO: Check if raw_input works for the EV3
    if not validateIPv4(host):
        print("Invalid IPv4-address, please try again.")
    else:
        break

port = 1234

s.connect((host, port))
print ((s.recv(1024)).decode('utf-8'))

pygame.init()

screen = pygame.display.set_mode((640,480)) # Set screen size of pygame window
background = pygame.Surface(screen.get_size())  # Create empty pygame surface
background.fill((255,255,255))     # Fill the background white color (red,green,blue)
background = background.convert()  # Convert Surface to make blitting faster

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
            elif event.key == pygame.K_UP:
                msg = 'fwd'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_DOWN:
                msg = 'bwd'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_LEFT:
                msg = 'left'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_RIGHT:
                msg = 'right'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_LSHIFT:
                msg = 'open'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_LCTRL:
                msg = 'close'
                print(msg)
                s.send(msg.encode('utf-8'))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                msg = 'stop'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_DOWN:
                msg = 'stop'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_LEFT:
                msg = 'stop'
                print(msg)
                s.send(msg.encode('utf-8'))
            elif event.key == pygame.K_RIGHT:
                msg = 'stop'
                print(msg)
                s.send(msg.encode('utf-8'))

    
    '''
    msg = input('Enter a command: ')
    if msg == '':
        break
    s.send(msg.encode('utf-8'))
    '''

pygame.display.quit()
pygame.quit()

s.close()
