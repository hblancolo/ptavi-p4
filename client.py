#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METOD = sys.argv[3].upper()  # upper me lo pone en mayusculas
    USER = sys.argv[4]
    EXPIRES = sys.argv[5]
    int(EXPIRES)
except:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    line = (METOD + ' sip:' + USER + ' SIP/2.0\r\nExpires: ' + EXPIRES)
    print("Enviando:", line)
    my_socket.send(bytes(line, 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)  # 1024 es el valor del buffer
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
