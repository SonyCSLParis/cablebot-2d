# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:38:31 2023

@author: angab
"""


import socket
import testT as te
import time


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
    

class EmmeteurT:
    def __init__(self, host, port,turn):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tour=turn
        
    def connect(self):
        self.socket.connect((self.h, self.p))
        print ("Connection on {}".format(self.p))
        return
    
    def end(self):
        print ("Close")
        mes="END"
        self.socket.sendall(mes.encode())
        self.socket.close()
        return
        
    def pilote(self, val, T):
        mes="G "+str(val)+" "+str(T)
        self.socket.sendall(mes.encode())
        turn=val*T
        self.tour+=turn
        return
    
    def switch(self, mode):
        mes="S "+mode
        self.socket.sendall(mes.encode())
        return
    def get_turn(self):
        return self.tour

class Cablebot:
    def __init__(self, Emet, long, larg, focus):
        self.Emet=Emet
        self.long=long
        self.larg=larg
        self.focus=focus
        self.Pos=None
        self.Tour=None
    
    def start(self):
        for i in self.Emet:
            i.connect()
        time.sleep(20)
        self.Pos=te.calcul_pos(self.long,self.larg,self.focus)
        Tour=[]
        for i in self.Emet:
            Tour.append(i.get_turn)
        self.Tour=Tour
        return 0
    
    def add_emet(self,emet):
        if len(self.Emet)==4:
            print("Deja trop de moteurs")
            return -1
        else:
            self.Emet.append(emet)
            return 0
    
    def quotidien(self):
        size=len(self.Emet)
        for i in range(len(self.Pos)):
            Point=self.Pos[i]
            Cons,self.Tour=te.calcul_pos_mot(Point,self.long,self.larg,self.Tour)
            for j in range(size):
                if Cons[j]<=0:
                    mode='t'
                    self.Emet[j].switch(mode)
                    Cons[j]=0.2
                else:
                    mode='v'
                    self.Emet[j].switch(mode)
            Time=[]
            for k in Cons:
                t=te.calc_t(k)
                Time.append(t)
            T=Time[0]
            for i in range(1,size):
                if Time[i]>T:
                    T=Time[i]
            
            for k in range(size):
                val=Cons[k]
                self.Emet[k].pilote(val,T)
        return 0
    
    def goto(self, x, y):
        Point=[x,y]
        size=len(self.Emet)
        Cons,self.Tour=te.calcul_pos_mot(Point,self.long,self.larg,self.Tour)
        for j in range(size):
            if Cons[j]<=0:
                mode='t'
                self.Emet[j].switch(mode)
                Cons[j]=0.2
            else:
                mode='v'
                self.Emet[j].switch(mode)
        Time=[]
        for k in Cons:
            t=te.calc_t(k)
            Time.append(t)
        T=Time[0]
        for i in range(1,size):
            if Time[i]>T:
                T=Time[i]
        
        for k in range(size):
            val=Cons[k]
            self.Emet[k].pilote(val,T)
        return 0
    
    
    def end(self):
        for i in self.Emet:
            i.end()
    
    """
    fonction temporaire pour tester la 2D
    """
    def line_test(self):
        Cons=te.pos_ligne()
        L=te.calcul_pos_mot_ligne(Cons)
        t1=self.Emet[0].get_turn()
        t2=self.Emet[1].get_turn()
        T=[t1,t2]
        Mot=te.calc_tour_ligne(L,T)
        for i in range (len(Mot)):
            for j in range(2):
                if (Mot[i][j]<=0):
                    mode='t'
                    self.Emet[j].switch(mode)
                    Mot[i][j]=0.2
                else:
                    mode='v'
                    self.Emet[j].switch(mode)
            
            t1=te.calc_t(Mot[i][0])
            t2=te.calc_t(Mot[i][1])
            T=t1
            if t2>t1:
                T=t2
            
            for j in range(2):
                val=Mot[i][j]
                self.Emet[j].pilote(val,T)
        return 0
    
    def speed(self, V, T):
        mode='v'
        for i in self.Emet:
            i.switch(mode)
        for i in range(len(self.Emet)):
            val=V[i]
            self.Emet[i].pilote(val,T)
        return 0



                
        