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

claw = ev3.MediumMotor('outA')
claw.run_timed(time_sp=2000, speed_sp=-500)
claw_open = True
left_motor = ev3.LargeMotor('outB')
right_motor = ev3.LargeMotor('outC')
camera = ev3.MediumMotor('outD')
lmax = left_motor.max_speed
rmax = right_motor.max_speed

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(('trololo').encode('utf-8'))
    while True:
        msg = (c.recv(1024)).decode('utf-8')
        for ch in msg:
            if ch == '':
                break
            elif ch == 'm':
                left_motor.run_forever(speed_sp=lmax)
                right_motor.run_forever(speed_sp=rmax)
            elif ch == 'n':
                left_motor.run_forever(speed_sp=-lmax)
                right_motor.run_forever(speed_sp=-rmax)
            elif ch == 'b':
                left_motor.run_forever(speed_sp=-lmax)
                right_motor.run_forever(speed_sp=rmax)
            elif ch == 'v':
                left_motor.run_forever(speed_sp=lmax)
                right_motor.run_forever(speed_sp=-rmax)
            elif ch == 'g':
                left_motor.stop()
                right_motor.stop()
            elif ch == 'l':
                left_motor.run_forever(speed_sp=lmax)
            elif ch == 'j':
                left_motor.run_forever(speed_sp=-lmax)
            elif ch == 'k':
                left_motor.stop()
            elif ch == 'r':
                right_motor.run_forever(speed_sp=rmax)
            elif ch == 'w':
                right_motor.run_forever(speed_sp=-rmax)
            elif ch == 'e':
                right_motor.stop()
            elif ch == '1':
                claw.run_timed(time_sp=2000, speed_sp=-500)
                claw_open = True
            elif ch == '2':
                claw.run_timed(time_sp=2000, speed_sp=500)
                claw_open = False
            elif ch == 'z':
                if claw_open:
                    claw.run_timed(time_sp=2000, speed_sp=500)
                    claw_open = False
                else:
                    claw.run_timed(time_sp=2000, speed_sp=-500)
                    claw_open = True
            elif ch == 'c':
                camera.run_timed(time_sp=100, speed_sp=200)
            elif ch == 'x':
                camera.run_timed(time_sp=100, speed_sp=-200)
            else:
                ev3.Sound.speak(msg).wait()
    c.close()



