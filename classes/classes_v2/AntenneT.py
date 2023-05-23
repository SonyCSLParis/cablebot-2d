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
        if test_mot < 0:
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
        print("Attention, vérifiés bien qu'un couple positif déroule le câble")
        
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
        print("message:",mes)
        self.socket.sendall(mes.encode())
        turn=val*T
        self.tour+=turn
        return
    
    def switch(self, mode):
        mes="S "+mode
        self.socket.sendall(mes.encode())
        return
    
    def set_tor(self,tor):
        mes="T "+str(tor)
        self.socket.sendall(mes.encode())
        
    def get_turn(self):
        return float(self.tour)



"""
CLASSE MAJEUR DU PROJET
"""


class Cablebot:
    def __init__(self, Emet, long, larg, focus):#Rajouter la cam quand OK
        #self.Cam=Cam
        self.Emet=Emet
        self.long=long
        self.larg=larg
        self.focus=focus
        self.Pos=None
        self.Tour=None
    
    def start(self):
        #self.Cam.connect()
        for i in self.Emet:
            i.connect()
        time.sleep(20)
        self.Pos=te.calcul_pos(self.long,self.larg,self.focus)
        Tour=[]
        for i in self.Emet:
            Tour.append(i.get_turn())
        self.Tour=Tour
        return 0
    
    def add_emet(self,emet):
        if len(self.Emet)==4:
            print("Deja trop de moteurs")
            return -1
        else:
            self.Emet.append(emet)
            return 0
    
    def pic(self):
        self.Cam.takepic()
        return
    
    def endrun(self):
        self.Cam.finparc()
        return
    
    def set_torques(self,TOR):
        l=len(self.Emet)
        for i in range(l):
            self.Emet[i].set_tor(TOR[i])
        return
    
    def quotidien(self):
        size=len(self.Emet)
        for i in range(len(self.Pos)):
            #print('tour ',i,'du parcours')
            Point=self.Pos[i]
            Cons,self.Tour=te.calcul_pos_mot(Point, self.long, self.larg, self.Tour)
            for j in range(size):
                if Cons[j]<=0:
                    mode='t'
                    self.Emet[j].switch(mode)
                    Cons[j]=0.1
                else:
                    mode='v'
                    self.Emet[j].switch(mode)
                time.sleep(1)
            
            Time=[]
            for k in Cons:
                t=te.calc_t(k)
                Time.append(t)
            T=Time[0]
            for i in range(1,size):
                if Time[i]>T:
                    T=Time[i]
            
            val1=Cons[0]
            if val1 !=0.1:
                val1=te.calc_vit(T, val1)
                
            val2=Cons[1]
            if val2 != 0.1:
                val2=te.calc_vit(T, val2)
                
            val3=Cons[2]
            if val3 != 0.1:
                val3=te.calc_vit(T, val3)
                
            val4=Cons[3]
            if val4 != 0.1:
                val4=te.calc_vit(T, val4)
                
            VAL=[val1,val2,val3,val4]
            for k in range(size):
                self.Emet[k].pilote(VAL[k],T)
            time.sleep(T)
            
            #self.pic()
        
        #self.endrun()
        return 0
    
    def goto(self, x, y):
        Point=[x,y]
        size=len(self.Emet)
        Cons,self.Tour=te.calcul_pos_mot(Point,self.long,self.larg,self.Tour)
        for i in range(size):
            if Cons[i]<=0:
                mode='t'
                self.Emet[i].switch(mode)
                Cons[i]=0.1
            else:
                mode='v'
                self.Emet[i].switch(mode)
            
        Time=[]
        for k in Cons:
            t=te.calc_t(k)
            Time.append(t)
        T=Time[0]
        for i in range(1,size):
            if Time[i]>T:
                T=Time[i]
        
        
        val1=Cons[0]
        if val1 !=0.1:
            val1=te.calc_vit(T, val1)
           
        val2=Cons[1]
        if val2 != 0.1:
            val2=te.calc_vit(T, val2)
           
        val3=Cons[2]
        if val3 != 0.1:
            val3=te.calc_vit(T, val3)
           
        val4=Cons[3]
        if val4 != 0.1:
            val4=te.calc_vit(T, val4)
           
        VAL=[val1,val2,val3,val4]
        for k in range(size):
            self.Emet[k].pilote(VAL[k],T)
        time.sleep(T)
        
        time.sleep(T)
        
        return 0
    
    def switch(self, Mode):
        l=len(self.Emet)
        T=[]
        V=[]
        for i in range(l):
            T.append('0')
            V.append('0')
        print("T: ",T)
        print("V: ",V)
        for i in range(l):
            mod=Mode[i]
            if mod=='t' or mod=='T':
                T[i]=mod
            else:
                V[i]=mod
        print("T': ",T)
        print("V': ",V)
        for i in range(l):
            modt=T[i]
            print("modt: ",modt)
            if modt!='0':    
                self.Emet[i].switch(modt)
            else:
                pass
        for i in range(l):
            modv=V[i]
            print('modv: ',modv)
            if modv!='0':    
                self.Emet[i].switch(modv)
            else:
                pass
        return 0
    
    
    def end(self):
        #self.Cam.end()
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
                if (Mot[i][j]<=0):#Passage en torque
                    mode='t'
                    self.Emet[j].switch(mode)
                    Mot[i][j]= -0.1
                else:
                    mode='v'
                    self.Emet[j].switch(mode)
                print(j,": mode ",mode)
            time.sleep(1)
            
            t1=te.calc_t(Mot[i][0])
            t2=te.calc_t(Mot[i][1])
            T=t1
            if t2>t1:
                T=t2
            
            val1=Mot[i][0]
            if val1 != -0.1:
                val1=(-1)*te.calc_vit(T, val1)
            
            val2=Mot[i][1]
            if val2 != -0.1:
                val2=(-1)*te.calc_vit(T, val2)
            
            print("val1: ",val1, " et val2: ",val2,"\n")
            self.Emet[0].pilote(val1,T)
            self.Emet[1].pilote(val2,T)
            time.sleep(T)
            
        return 0
    
    def speed(self, V, T):
        mode='v'
        for i in self.Emet:
            i.switch(mode)
        time.sleep(1)
        
        for i in range(len(self.Emet)):
            val=V[i]
            self.Emet[i].pilote(val,T)
        time.sleep(1)
        
        return 0
                

class EmmetCam:
    def __init__(self, host, port):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.socket.connect((self.h, self.p))
        print ("Connection on {}".format(self.p))
        return        
    
    def takepic(self):
        mes='2'
        self.socket.sendall(mes.encode())
        time.sleep(5)
        return
    
    def finparc(self):
        mes='1'
        self.socket.sendall(mes.encode())
        return
    
    def end(self):
        self.socket.close()
        print("Caméra déconnectée")
        return
        
        
        