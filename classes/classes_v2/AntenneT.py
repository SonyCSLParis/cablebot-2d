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
    

class EmmeteurT:
    def __init__(self, host, port,turn):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tour=turn
        print("Attention, vérifiés bien qu'un couple positif enroule le câble")
        
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
    
    def speed(self,v):
        mes="V "+str(v)
        self.socket.sendall(mes.encode())
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
    
    def set_turn(self,turn):
        self.tour=turn
        return



"""
CLASSE MAJEUR DU PROJET
"""


class Cablebot:
    def __init__(self,Cam , Emet, long, larg, focus):#Rajouter la cam quand OK
        self.Cam=Cam
        self.Emet=Emet
        self.long=long
        self.larg=larg
        self.focus=focus
        self.Pos=None
        self.Tour=None
        self.conv=0.2
    
    def start(self):
        if self.Cam != None:
            self.Cam.connect()
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
    
    def set_tour(self):
        Tour=[]
        for i in self.Emet:
            Tour.append(i.get_turn())
        self.Tour=Tour
        return 
    
    def quotidien(self):
        size=len(self.Emet)
        x=float(input("Quel x de départ? \n"))
        y=float(input("Quel y de départ? \n"))
        ORIGINE=te.calcul_long_mot([x,y],self.long,self.larg)
        
        #Definir le tour initial de chaque moteur 
        self.reset_mot(ORIGINE)
        
        for i in range(len(self.Pos)):
            
            #debugage
            print("\n")
            print('tour ',i,'du parcours')
            print("\n")
            
            
            #on recupere le point de l'étape
            Point=self.Pos[i]
            Cons,self.Tour=te.calcul_pos_mot(Point, self.long, self.larg, self.Tour)
            print("Cons: ",Cons)
            print("\n")
            Mod=[]
            for j in range(size):
                if Cons[j]>=0:
                    mode='t'
                    Cons[j]=-0.1
                else:
                    mode='v'
                Mod.append(mode)
            print("Mod: ",Mod,"\n")
            #MàJ des modes de chaque moteur
            self.switch(Mod)
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
            if val1 !=-0.1:
                val1=te.calc_vit(T, val1)
                
            val2=Cons[1]
            if val2 !=-0.1:
                val2=te.calc_vit(T, val2)
                
            val3=Cons[2]
            if val3 !=-0.1:
                val3=te.calc_vit(T, val3)
                
            val4=Cons[3]
            if val4 !=-0.1:
                val4=te.calc_vit(T, val4)
                
            VAL=[val1,val2,val3,val4]
            for k in range(size):
                self.Emet[k].pilote(VAL[k],T)
            time.sleep(T)
            
            #self.takepic()
        
        #self.endrun()
        return 0
    
    def goto(self, x, y):
        Point=[x,y]
        size=len(self.Emet)
        
        #definir la position d'origine
        x=float(input("Quel x de départ? \n"))
        y=float(input("Quel y de départ? \n"))
        ORIGINE=te.calcul_long_mot([x,y],self.long,self.larg)
        
        #Definir le tour initial de chaque moteur 
        self.reset_mot(ORIGINE)
        
        Cons,self.Tour=te.calcul_pos_mot(Point,self.long,self.larg,self.Tour)
        Mod=[]
        for i in range(size):
            if Cons[i]>=0:
                mode='t'
                Cons[i]=-0.1
            else:
                mode='v'
            Mod.append(mode)  
        self.switch(Mod)
        
        Time=[]
        for k in Cons:
            t=te.calc_t(k)
            Time.append(t)
        T=Time[0]
        for i in range(1,size):
            if Time[i]>T:
                T=Time[i]
        
        
        val1=Cons[0]
        if val1 !=-0.1:
            val1=te.calc_vit(T, val1)
           
        val2=Cons[1]
        if val2 !=-0.1:
            val2=te.calc_vit(T, val2)
           
        val3=Cons[2]
        if val3 != -0.1:
            val3=te.calc_vit(T, val3)
           
        val4=Cons[3]
        if val4 != -0.1:
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
        #print("T: ",T)
        #print("V: ",V)
        #print("\n")
        for i in range(l):
            mod=Mode[i]
            if mod=='t' or mod=='T':
                T[i]=mod
            else:
                V[i]=mod
        print("T': ",T)
        print("V': ",V)
        print("\n")
        
            
        for i in range(l):
            modt=T[i]
            #print("modt: ",modt)
            if modt!='0':    
                self.Emet[i].switch(modt)
            else:
                pass
        for i in range(l):
            modv=V[i]
            #print('modv: ',modv)
            #print("\n")
            if modv!='0':    
                self.Emet[i].switch(modv)
            else:
                pass
        return 0
    
    def takepic(self):
        for i in self.Emet:
            i.switch('t')
            time.sleep(1)
        for i in self.Emet:
            i.switch('v')
            time.sleep(1)
        time.sleep(1)
        print("prise de photo")
        print("\n")
        self.Cam.takepic()
        return 
        
    def end(self):
        if self.Cam != None:
            self.Cam.end()
        for i in self.Emet:
            i.end()
    
    def reset_mot(self,L):
        for i in range(len(self.Emet)):
            turn=L[i]/self.conv
            self.Emet[i].set_turn(turn)
            self.set_tour()
    
    
    def speed(self,V):
        for i in range(len(self.Emet)):
            val=V[i]
            self.Emet[i].speed(val)
        time.sleep(1)
        
    def pilote(self, V, T):
        for i in range(len(self.Emet)):
            val=V[i]
            self.Emet[i].pilote(val,T)
        time.sleep(1)
        
        return 0

    """
    fonction temporaire pour tester la 2D
    """
    def plan_test(self):
        Cons=te.pos_plan()
        L=te.calcul_pos_mot_plan(Cons)
    
        #Définir la position de départ
        x=float(input("Quel x de départ? \n"))
        y=float(input("Quel y de départ? \n"))
        ORIGINE=te.calcul_pos_mot_plan([(x,y)])
    
        #Definir le tour initial de chaque moteur 
        self.reset_mot(ORIGINE)
    
        #début du test
        t1=self.Emet[0].get_turn()
        t2=self.Emet[1].get_turn()
        #T=[5,5]#temporaire à remplacer par le bon homing
        Mot=te.calc_tour_plan(L,[t1,t2],self.conv)
        for i in range (len(Mot)):
            Mod=[]
            print("Consigne ",i,"en cours: ",Mot[i],"\n")
            for j in range(2):
            
                if (Mot[i][j]>=0):#Passage en torque
                    mode='t'
                    Mot[i][j]=-0.1
                else:
                    mode='v'
                print(j,": mode ",mode)
                Mod.append(mode)
            self.switch(Mod)
            time.sleep(1)
        
            t1=te.calc_t(Mot[i][0])
            t2=te.calc_t(Mot[i][1])
            T=t1
            if t2>t1:
                T=t2
        
            val1=Mot[i][0]
            if val1 != -0.1:
                val1=te.calc_vit(T, val1)
        
            val2=Mot[i][1]
            if val2 != -0.1:
                val2=te.calc_vit(T, val2)
            print("val1: ",val1, " et val2: ",val2,"\n")
            print("T=",T)
            self.Emet[0].pilote(val1,T)
            self.Emet[1].pilote(val2,T)
            time.sleep(T)
            self.takepic()
            self.Cam.finparc()
        
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
        time.sleep(10)
        return
    
    def finparc(self):
        mes='1'
        print('Fin de parcours')
        self.socket.sendall(mes.encode())
        time.sleep(5)
        return
    
    def end(self):
        self.socket.close()
        print("Caméra déconnectée")
        return
        
        
        