# -*- coding: utf-8 -*-
"""
Created on Wed May 31 17:30:17 2023

@author: angab
"""
import socket

class AntenneT:
    def __init__(self,mot,port):
        self.mot=mot
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        #on attribue un port à notre serveur
        self.socket.listen(5)
        #5 connexions pendantes
        self.client, self.address = self.socket.accept()
    
    def init(self):
        test=self.mot.set_config()
        if test==-1:
            print("ERREUR")
        return
    
    def run(self):
        print ("{} connected".format( self.address ))
        a=True
        self.mot.get()
        #print(self.mot.odrv)
        """ if test_mot < 0:
            print("erreur moteur non attaché")
            print ("Close")
            self.client.close()
            self.socket.close()
            return"""
        
        while a==True:
                mes = self.client.recv(255)
                mes=str(mes)
                if mes != "b''":
                    test=self.mot.run_m(mes)
                    print("test: ", test)
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
