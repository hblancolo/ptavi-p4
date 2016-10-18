#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import sys
import socket

# Constantes. Dirección IP del servidor y contenido a enviar
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
METOD = sys.argv[3]
USER = sys.argv[4]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    line_send = METOD + ' sip:' + USER + ' SIP/2.0\r\n\r\n'
    print("Enviando:", line_send)
    my_socket.send(bytes(line_send, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)  # 1024 es el valor del buffer
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
