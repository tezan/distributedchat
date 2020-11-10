#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback
from termcolor import colored

class Server(threading.Thread):
    def initialise(self,receive):
        self.receive=receive
    
    def run(self):
        lis=[]
        lis.append(self.receive)
        while 1:
            read,write,err=select.select(lis,[],[])
            for item in read:
                try:
                    s=item.recv(1024)
                    if s!='':
                        chunk=s                
                        print(str('')+':'+chunk)
                except:
                    traceback.print_exc(file=sys.stdout)
                    break

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))
    def client(self,host,port,msg):               
        sent=self.sock.send(msg)           
        #print "Sent\n"
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host=input("Ingresa el nombre del host\n>>")            
            port=int(input("Ingresa el puerto a utilizar\n>>"))
        except EOFError:
            print("Algo salió mal.")
            return 1
        
        print("Conectando...", end="", flush=True)
        s=''
        self.connect(host,port)
        print(colored('      [OK]', 'green'))
        print("Iniciando el servicio...", end="", flush=True)
        receive=self.sock
        time.sleep(1)
        srv=Server()
        srv.initialise(receive)
        srv.daemon=True
        srv.start()
        print(colored('      [OK]', 'green'))
        print("===============================================\nBienvenido al chat P2P más horrendo del universo.\nEnvía 'quit' sin comillas para salir")
        while 1:            
            msg=input('>>')
            if msg=='quit':
                break
            if msg=='':
                continue
            self.client(host,port,msg.encode())
        return(1)
if __name__=='__main__':
    print("Iniciando el cliente...")
    cli=Client()    
    cli.start()
