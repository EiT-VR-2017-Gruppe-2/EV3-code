# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket

s = socket.socket()
#host = socket.gethostname()
host = '192.168.137.3'
port = 1234

s.connect((host, port))
print ((s.recv(1024)).decode('utf-8'))
s.close()