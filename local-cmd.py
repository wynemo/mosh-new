#!/usr/bin/env python

import socket
import base64
import json

__author__ = 'nemo.zhang'

CONFIG_FILE = 'config.json'


with open(CONFIG_FILE, 'rb') as f:
    o = json.load(f)
    server = o['server']
    port = o['server_port']

def encode(s):
    return base64.b64encode(s, b'`!')


def decode(s):
    return base64.b64decode(s, b'`!')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)
s.sendto(encode('mosh-server'), (server, port))
data, _ = s.recvfrom(64*1024)
print(decode(data))
