# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket
import pygame

import sys
import time
import openvr
import math

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

def GetYawValue(yaw1, yaw2):
    if (yaw1 >= 0 and yaw2 >= 0):
        return yaw1/2
    elif(yaw1 >= 0 and yaw2 < 0):
        return 1-(yaw1/2)
    elif(yaw1 < 0 and yaw2 < 0):
        return -0.5+(yaw2/2)
    elif(yaw1 < 0 and yaw2 >= 0):
        return -0.5+(yaw2/2)

def GetOffsetYawValue(value, offset):
    v = value-offset
    if v < -1:
        v = 2+v
    elif v > 1:
        v = v-2
    return round(v, 2)

def GetDistance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

#Socket setup
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

#Pygame setup
pygame.init()

screen = pygame.display.set_mode((640,480)) # Set screen size of pygame window
background = pygame.Surface(screen.get_size())  # Create empty pygame surface
background.fill((255,255,255))     # Fill the background white color (red,green,blue)
background = background.convert()  # Convert Surface to make blitting faster

#VR Setup
openvr.init(openvr.VRApplication_Scene)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()

openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
yaw1 = (poses[0].mDeviceToAbsoluteTracking)[2][0]
yaw2 = (poses[0].mDeviceToAbsoluteTracking)[2][2]
offset = GetYawValue(yaw1, yaw2)
previous_view = offset

loop = True
while loop:
    # Keyboard events
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

    #VR events
    openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    headset_tracking = poses[0].mDeviceToAbsoluteTracking
    controller1_tracking = poses[3].mDeviceToAbsoluteTracking
    controller2_tracking = poses[2].mDeviceToAbsoluteTracking
    yaw1 = headset_tracking[2][0]
    yaw2 = headset_tracking[2][2]
    yaw_value = GetYawValue(yaw1,yaw2)
    #print(yaw_value)
    #print(GetOffsetYawValue(yaw_value, offset))
    #print('')

    current_view = GetOffsetYawValue(yaw_value, offset)

    diff = ((current_view) - (previous_view))
        
    if ((diff < 0.05) and (diff > -0.05)):
        print('Nothing')
    else:
        print('Changed')

        if diff > 0.0:
            msg = 'cr'
            print(msg)
            s.send(msg.encode('utf-8'))
        else:
            msg = 'cl'
            print(msg)
            s.send(msg.encode('utf-8'))
        
        previous_view = current_view
    print('')

    headset_x = headset_tracking[2][3]
    headset_y = headset_tracking[0][3]

    controller1_x = controller1_tracking[2][3]
    controller1_y = controller1_tracking[0][3]

    controller2_x = controller2_tracking[2][3]
    controller2_y = controller2_tracking[0][3]

    distance1 = GetDistance(headset_x, headset_y, controller1_x, controller1_y)
    distance2 = GetDistance(headset_x, headset_y, controller2_x, controller2_y)

    event = openvr.VREvent_t()
    while(openvr.VRSystem().pollNextEvent(event)):
        t = event.eventType
        if (t == openvr.VREvent_ButtonPress and event.data.controller.button == openvr.k_EButton_SteamVR_Trigger):
            msg = 'claw'
            print(msg)
            s.send(msg.encode('utf-8'))
    
    sys.stdout.flush()
    time.sleep(0.2)

    
    '''
    msg = input('Enter a command: ')
    if msg == '':
        break
    s.send(msg.encode('utf-8'))
    '''

openvr.shutdown()
pygame.display.quit()
pygame.quit()

s.close()
