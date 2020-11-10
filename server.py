#! /usr/bin/env python

import socket
import sys, traceback
import threading
import select
from termcolor import colored

sockets=[]
outwardsContent=[]
sender={}

class Server(threading.Thread):

    def init(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('',5535))
        self.sock.listen(2)
        sockets.append(self.sock)
        
        print("Iniciando servidor en puerto 5535", colored('      [OK]', 'green'))

    def run(self):
        while 1:
            read,write,err=select.select(sockets,[],[],0)     
            for sock in read:
                if sock==self.sock:                    
                    sockfd,addr=self.sock.accept()
                    print(addr)
                    sockets.append(sockfd)
                    print(str(sockets[len(sockets)-1]))
                else:
                    try:
                        s=sock.recv(1024)
                        if s=='':
                            print(str(sock.getpeername()))                            
                            continue
                        else:
                            outwardsContent.append(s)  
                            sender[s]=(str(sock.getpeername()))
                    except:
                        print(str(sock.getpeername()))                    
                    
            
class handle_connections(threading.Thread):
    def run(self):        
        while 1:
            read,write,err=select.select([],sockets,[],0)
            for items in outwardsContent:
                for s in write:
                    try:
                        if(str(s.getpeername()) == sender[items]):
                        	print("Ignoring %s"%(str(s.getpeername())))
                        	continue
                        print("Sending to %s"%(str(s.getpeername())))
                        s.send(items)                                             
                        
                    except:
                        traceback.print_exc(file=sys.stdout)
                outwardsContent.remove(items)   
                del(sender[items])              
                


if __name__=='__main__':
    srv=Server()
    srv.init()
    srv.start()
    print(sockets)
    handle=handle_connections()    
    handle.start()   
