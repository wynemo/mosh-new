#!/usr/bin/env python

import socket
import base64
import subprocess
import os
import termios
import struct
import fcntl
import signal
import time

__author__ = 'nemo.zhang'


def encode(s):
    return base64.b64encode(s, b'`!')


def decode(s):
    return base64.b64decode(s, b'`!')


def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


signal.signal(signal.SIGHUP, lambda x, y: None)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 50232))

while 1:
    data, address = s.recvfrom(64*1024)
    cmd = decode(data)
    if cmd == b'mosh-server':
        pid, fd = os.forkpty()
        if pid == 0:
            time.sleep(1)
            data = subprocess.getoutput('/usr/bin/mosh-server')
            print(data)
            exit(0)
        else:
            set_winsize(fd, 32, 100)
            os.waitpid(pid, 0)
            data = os.read(fd, 1024)
            s.sendto(encode(data), address)
