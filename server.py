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
left_motor = ev3.LargeMotor('outB')
right_motor = ev3.LargeMotor('outC')

#m.run_timed(time_sp=3000, speed_sp=500)


while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(('trololo').encode('utf-8'))
    while True:
        msg = (c.recv(1024)).decode('utf-8')
        if msg == '':
            break
        elif msg == 'fwd':
            left_motor.run_forever(speed_sp=500)
            right_motor.run_forever(speed_sp=500)
        elif msg == 'bwd':
            left_motor.run_forever(speed_sp=-500)
            right_motor.run_forever(speed_sp=-500)
        elif msg == 'left':
            left_motor.run_forever(speed_sp=-500)
            right_motor.run_forever(speed_sp=500)
        elif msg == 'right':
            left_motor.run_forever(speed_sp=500)
            right_motor.run_forever(speed_sp=-500)
        elif msg == 'stop':
            left_motor.stop()
            right_motor.stop()
        elif msg == 'open':
            claw.run_timed(time_sp=3000, speed_sp=-500)
        elif msg == 'close':
            claw.run_timed(time_sp=3000, speed_sp=500)
        else:
            ev3.Sound.speak(msg).wait()
    c.close()


