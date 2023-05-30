# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:38:31 2023

@author: angab
"""


import socket
import testT as te
import time
import math
#import keyboard

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
        
        #DATA
        self.kNord = [0, 0]
        self.kOuest = [3, 0]
        self.kEst = [0, 3]
        self.kSud = [3, 3]
        self.kDistancePerTurn = 0.075
    
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
        time.sleep(1)
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
            #time.sleep(1)
            
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
        time.sleep(1)
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
        if self.Cam != None:
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
        #time.sleep(0.5)
        
        return 0
    
    

    def distance(self,a, b):
         dx = a[0] - b[0]
         dy = a[1] - b[1]
         return math.sqrt(dx * dx + dy * dy)

    def unwind(self,reference, position, target):
         distance_start = self.distance(reference, position)
         distance_end = self.distance(reference, target)
         return distance_end - distance_start

    def compute_unwind(self,position, target):
         nord = self.unwind(self.kNord, position, target)
         ouest = self.unwind(self.kOuest, position, target)
         est = self.unwind(self.kEst, position, target)
         sud = self.unwind(self.kSud, position, target)
         return [nord, ouest, est, sud]

    def compute_turns(self,distances):
         return [distance / self.kDistancePerTurn for distance in distances]

    def compute_speeds(self,turns, dt):
         return [turn / dt for turn in turns]

    def compute_speeds_from_positions(self,position, target, dt):
         distances = self.compute_unwind(position, target)
         turns = self.compute_turns(distances)
         speeds = self.compute_speeds(turns, dt)
         return speeds

    def estimate_new_position(self,position, dx):
         return [position[0] + dx[0], position[1] + dx[1]]

    def sleep(self,dt):
         time.sleep(dt)


    def stop(self):
         self.pilote([0, 0, 0, 0], 1.0)

    def compute_travel(self,position, target, duration, dt):
         dx = dt * (target[0] - position[0]) / duration
         dy = dt * (target[1] - position[1]) / duration
         return [dx, dy]

    def travel(self,position, target, duration):
        speeds = self.compute_speeds_from_positions(position, target, duration)
        print("speeds initiales: ",speeds)
        Mod=[]
        x=target[0]
        y=target[1]
        S_dead=0 # start dead zone
        E_dead=0.8 #end dead zone
        if S_dead <= x <= E_dead or S_dead <= y <= E_dead:
            tor=-0.05
        else:
            tor=-0.1
        TOR=[tor,tor,tor,tor]
        self.set_torques(TOR)
        for i in range (4):
            if speeds[i]<0:
                mod='v'
            else:
                mod='t'
            Mod.append(mod)
        print("Mod initial: ",Mod)
        self.switch(Mod)
        #time.sleep(1)
        delta_t = 2 # seconds
        delta_x = self.compute_travel(position, target, duration, delta_t)
        j=0
        while duration > 0:
            #if keyboard.is_pressed('space'):
                #self.speed([0,0,0,0])
               # break
            self.pilote(speeds, delta_t)
            self.sleep(1)
            duration = duration - delta_t
            if duration > 0:
                next_position = self.estimate_new_position(position, delta_x)
                distances = self.compute_unwind(position, next_position)
                turns = self.compute_turns(distances)
                speeds = self.compute_speeds(turns, delta_t)
                print("speeds ",j," : ",speeds)
                Mod=[]
                for i in range (4):
                    if speeds[i]<0:
                        mod='v'
                    else:
                        mod='t'
                    Mod.append(mod)
                print("Mod ",i,"")
                self.switch(Mod)
                position = next_position
                print(f'--\nPosition {position}\nDistances{distances}\nTurns {turns}\nSpeeds {speeds}')
            else:
                self.stop()
                j+=1
    """
    fonction temporaire pour tester la 2D
    """
    def plan_test(self):
        Cons=te.pos_plan()
        T=10
        for i in range(1,len(Cons)):
            pt_start=Cons[i-1]
            pt_goal=Cons[i]
            self.travel(pt_start,pt_goal,T)
            self.takepic()
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
        
        
        