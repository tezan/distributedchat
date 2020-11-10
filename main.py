#! /usr/bin/env python

import socket
import sys
import time
import threading
from termcolor import colored

class Server(threading.Thread):
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname=''
        port=51412
        self.sock.bind((hostname,port))
        self.sock.listen(1)     
        time.sleep(2)    
        (clientname,address)=self.sock.accept()
        print("Conexión desde %s\n" % str(address))        
        while 1:
            chunk=clientname.recv(4096)            
            print(str(address)+':'+ str(chunk))

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))
    def client(self,host,port,msg):               
        sent=self.sock.send(msg)           
        print("Enviado\n")
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            host=input("Ingresa el nombre del host \n>>")            
            port=int(input("Ingresa el puerto a utilizar \n>>"))
        except EOFError:
            print("Error")
            return 1
        
        print("Conectando...", end="", flush=True)
        s=''
        self.connect(host,port)
        print(colored('      [OK]', 'green'))
        print("===============================================\nBienvenido al chat P2P más horrendo del universo.\nEnvía 'quit' sin comillas para salir")
        while 1:            
            print("Esperando un mensaje...\n")
            msg=input('>>')
            if msg=='exit':
                break
            if msg=='':
                continue
            self.client(host,port,msg.encode())
        return(1)
if __name__=='__main__':
    srv=Server()
    srv.daemon=True
    print("Iniciando servidor en puerto 51412...", end="", flush=True)
    srv.start()
    time.sleep(1)
    print(colored('      [OK]', 'green'))
    print("Iniciando cliente...", end="", flush=True)
    cli=Client()
    print(colored('      [OK]', 'green'))
    cli.start()
