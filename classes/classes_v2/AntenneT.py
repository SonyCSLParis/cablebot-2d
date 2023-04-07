# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:38:31 2023

@author: angab
"""

import time 
import socket

def pause(t):
    time.sleep(t)


class AntenneT:
    def __init__(self,mot,port):
        self.mot=mot
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        #on attribue un port à notre serveur
        self.socket.listen(5)
        #5 connexions pendantes
        self.client, self.address = self.socket.accept()
        
    def run(self):
        print ("{} connected".format( self.address ))
        a=True
        test_mot=self.mot.get()
        while self.mot.state==True:
            pass
        while self.mot.state==False:
            pass
        if test_mot <0:
            print("erreur moteur non attaché")
            print ("Close")
            self.client.close()
            self.socket.close()
            return
        while a==True:
                mes = self.client.recv(255)
                mes=str(mes)
                if mes != "b''":
                    test=self.mot.run_m(mes)
                    while self.mot.state==False:
                        pause(0.05)
                    if test==False:
                        print("fermeture de serveur")
                        self.socket.settimeout(1)
                        a=False
                else:
                    a=False
        print ("Close")
        self.client.close()
        self.socket.close()
        return
    

class EmmeteurT:
    def __init__(self, host, port):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.socket.connect((self.h, self.p))
        print ("Connection on {}".format(self.p))
        return
    
    def end(self):
        print ("Close")
        mes="END"
        self.socket.send(mes.encode())
        self.socket.close()
        return
        
    def pilote(self, val, T, mode):
        mes="S "+mode
        self.socket.send(mes.encode())
        mes="G "+str(val)+" "+str(T)
        self.socket.send(mes.encode())
        time.sleep(0.5)
        return
    
    def resume(self):
        mes="R"
        self.socket.send(mes.encode())
        time.sleep(0.2)
        return
        