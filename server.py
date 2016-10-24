#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import sys
import socketserver
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    dic = {}  # almacena nombre usuario e ip correspondiente cuando REGISTER

    def check_expires(self):
        expired_users = []
        for usuario in self.dic:
            time_now = time.strftime('%Y-%m-%d %H:%M:%S', 
                                     time.gmtime(time.time()))
            if time_now >= self.dic[usuario][1]['expires']:
                expired_users.append(usuario)

        for usuario in expired_users:
            del self.dic[usuario]

    def register2json(self):
        fich_json = open('registered.json', 'w')
        codigo_json = json.dumps(self.dic)
        fich_json.write(codigo_json)
        fich_json.close()

    def json2registered(self):
        try:
            fich_json = open('registered.json', 'r')
            self.dic = json.load(fich_json)
        except:
            pass

    def handle(self):  # se ejecuta cada vez que server reciba petición
        line_str = self.rfile.read().decode('utf-8') 
        list_linecontent = line_str.split()
        self.json2registered()
        if list_linecontent[0] == 'REGISTER':
            user = list_linecontent[1].split(':')[-1]
            ip_user = self.client_address[0]
            if list_linecontent[3] == 'Expires:':
                expires = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(time.time() + 
                                        int(list_linecontent[4])))
                self.dic[user] = [{'address': ip_user}, {'expires': expires}]

                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        self.check_expires()
        self.register2json()
        print(self.dic)
if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
