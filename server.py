#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import sys
import socketserver


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    dic = {}  # almacena nombre usuario e ip correspondiente cuando REGISTER

    def handle(self):  # se ejecuta cada vez que server reciba petición
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        for line in self.rfile:
            line_str = line.decode('utf-8')
            if line_str != '\r\n':
                print('Dir. IP y puerto del cliente:', self.client_address)
                print("El cliente nos manda", line.decode('utf-8'))
                metod = line_str.split(' ')[0]
                user = line_str.split(' ')[1].split(':')[-1]
                SIPRegisterHandler.dic[user] = metod

            

        print(SIPRegisterHandler.dic)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
