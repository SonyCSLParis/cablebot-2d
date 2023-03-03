# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:38:45 2023

@author: angab
"""

import socket

class RemoteMotor:
    def __init__(self, Motor):
        self.mot=Motor#Moteur piloté par la remote
        self.c=""#
    
    def on(self):
        self.mot.get()
        
    def inter_mes(self, message):
        mode=message[2]
        
        """
        Cas END
        """
        if (mode=="E"):
            resp=self.end()
        
        """
        Cas Pilotage
        """
        if (mode=="P"):
            i=4
            test=message[i]
            vit=[]
            while (test!=" "):
                i=i+1
                vit.append(test)
                test=message[i]
            vit=float("".join(vit))
            
            i=i+1
            test=message[i]
            T=[]
            while (test!="&"):
                i=i+1
                T.append(test)
                test=message[i]
            T=int("".join(T))
            resp=self.pilotage(vit,T)
            
        return resp
    
    
    def end(self):
        print("arrêt moteur")
        return False
    
    def pilotage(self,vit,T):
        self.mot.moveto(vit,T)
        return True
            
            
class ProxyMotor:
    def __init__(self, host, port, xmax, ymax):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.xmax=xmax
        self.ymax=ymax
        self.tour=0
        
    def connect(self,tour):
        self.socket.connect((self.h, self.p))
        print ("Connection on {}".format(self.p))
        self.tour=tour
    
    
    
    def end(self):
        print ("Close")
        mes="END"
        self.socket.send(mes.encode())
        self.socket.close()
        
    def pilote(self,v,t):
        self.tour=self.tour+v*t
        mes="P "+str(v)+" "+str(t)+"&"
        self.socket.send(mes.encode())



class Antenne:
    def __init__(self,port,Remote):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        #on attribue un port à notre serveur
        self.socket.listen(5)
        #5 connexions pendantes
        self.client, self.address = self.socket.accept()
        self.R=Remote
    
    def run(self):
        self.R.on()
        print ("{} connected".format( self.address ))
        a=True
        while a==True:
                mes = self.client.recv(255)
                mes=str(mes)
                if mes != b'':
                    test=self.R.inter_mes(mes)
                    print("test :",test)
                    if test==False:
                        print("fermeture de serveur")
                        self.socket.settimeout(1)
                        a=False
        print ("Close")
        self.client.close()
        self.socket.close()
        return