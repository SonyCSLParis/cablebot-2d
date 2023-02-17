# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:51:10 2023

@author: angab
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:26:25 2023

@author: angab
"""
import odrive
#import odrive.enmus as od
import os 
import cv2 as cv
import time
import math as mp
import threading as th


def pause(t = 0.1):
    """
    pas grand-chose à ajouter...
    """
    #print("Pause started")
    time.sleep(t)
    #print("Pause ended")
    return None

def calcul_pos_mot(L, lon, lar, Tour):
     Mot=[[0,0,0,0]]*len(L)
     Lon=[[0,0,0,0]]*len(L)
     k1=Tour[0]
     k2=Tour[1]
     k3=Tour[2]
     k4=Tour[3]
     for i in range (len(L)):
         y=L[i][0]
         x=L[i][1]
         d=0.5
         Conv=0.25
         #print(x,y)
         l1=mp.sqrt(x**2+y**2)
         l1=mp.sqrt(l1**2+d**2)
         #plt.plot(i,l1,color='red',marker='x')
         l2=mp.sqrt((lon-x)**2+y**2)
         l2=mp.sqrt(l2**2+d**2)
         #plt.plot(i,l2,color='green',marker='x')
         l3=mp.sqrt(x**2+(lar-y)**2)
         l3=mp.sqrt(l3**2+d**2)
         #plt.plot(i,l3,color='blue',marker='x')
         l4=mp.sqrt((lon-x)**2+(lar-y)**2)
         l4=mp.sqrt(l4**2+d**2)
         #plt.plot(i,l4,color='yellow',marker='x')
         Lon[i]=[l1,l2,l3,l4]
         #0,5 à changer car juste le rapport de m.tour-1
         c1=round((l1/Conv)-k1)
         c2=round((l2/Conv)-k2)
         c3=round((l3/Conv)-k3)
         c4=round((l4/Conv)-k4)
         k1=l1/Conv
         k2=l2/Conv
         k3=l3/Conv
         k4=l4/Conv
         Mot[i]=[c1,c2,c3,c4]
     return Mot

 #interpolatoin via les vitesses de chaque moteur et une constante de temps
def interpol(L):
     vel_max=10
     Vel=[[0, 0, 0, 0]]*len(L)
     for i in range(len(L)):
         V1=0
         V2=0
         V3=0
         V4=0
         C=L[i]
         maxi=abs(C[0])
         for j in C:
             if abs(j)>=maxi:
                 maxi=abs(j)
         T=maxi/vel_max #temps en seconde
         V1=C[0]/T
         V2=C[1]/T
         V3=C[2]/T
         V4=C[3]/T
         Vel[i]=[V1, V2, V3, V4,int(T)]
     return Vel
'''
class Motor(th.Thread):
    def __init__(self, serial, vmax, cmax, identifiant):
        th.Thread.__init__(self)
        self.serial = serial #numéro de série
        self.vmax = vmax #vitesse max
        self.cmax = cmax #courant max
        self.id = identifiant #numéro d'id du moteur
        self.odrv #futur objet qui accrochera le moteur odrive
        self.pos=0 #nombre de tour que le moteur a fait
        self.v=0 #consigne de vitesse
        self.T #constante de temsp
        self.etat = False #indicateur de l'état du moteur 
        self.go=False #le moteur doit fonctionner si go=True
        self.on=True #moteur allumé
    
    def run(self):
        #initialisation des moteurs attention prends du temps (30sec)
        self.odrv=odrive.find_any(self.serial)#attache du moteur
        ax = self.odrv.axis0
        ax.motor.config.pole_pairs = True
        self.odrv.config.dc_bus_overvoltage_trip_level = 40
        self.odrv.config.dc_max_positive_current = self.cmax#courant max
        ax.controller.config.vel_limit = self.vmax#vitesse max
        self.odrv.config.dc_max_negative_current = -1
        self.odrv.config.brake_resistor0.resistance = 2
        self.odrv.config.brake_resistor0.enable = True
        ax.config.motor.motor_type = od.MotorType.HIGH_CURRENT
        ax.config.motor.pole_pairs = 7
        ax.config.motor.torque_constant = 8.27 / 150
        ax.requested_state = od.AxisState.MOTOR_CALIBRATION #calibration des axes qui prends un certains temps
        pause(10)
        self.odrv.inc_encoder0.config.cpr = 8192
        self.odrv.inc_encoder0.config.enabled = True
        ax.requested_state = od.AxisState.ENCODER_INDEX_SEARCH #création de l'index de notre encodeur
        pause(10)
        ax.requested_state = od.AxisState.ENCODER_OFFSET_CALIBRATION#calcul de l'offset de l'encodeur
        pause(10)
        self.odrv.save_configuration()#sauvegarde de la config pour na pas avoir à la refaire après
        
        
        #démarer la closed loop de contrôle
        print("GO")
        ax=self.odrv.axis0
        ax.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
       
        #fonction pour se déplacer à un point de coordonnées x,y
  
        while (self.on==True):
            if (self.go==False):
                self.odrv.axis0.controller.input_vel = 0
            if (self.go==True):
                self.etat=True
                self.odrv.axis0.controller.input_vel =self.v
                self.pos=self.pos+(self.v*self.T)
                pause(self.T)
                self.odrv.axis0.controller.input_vel = 0
                self.go=False
            self.etat=False
        #implémenter une fonction qui attends que tous les moteurs soient avec un flag GO
        #puis qui fait tourner le moteur à la vitesse v pendant T secondes 
        #puis elle envoie un flag "fait"
        #et elle se remet en standby
        print("fait")
        
        
    def off(self):
        #detacher le moteur et l'éteindre
        print("Bye")
    
    #idée de def status(self): qui renvoit juste le state du moteur pour que l'on sache quand on peut envoyer la commande suivante
'''
class RemoteMotor:
    
    def __init__(self, Motors, large, long, vmax):
        self.Motors=Motors#listes des moteurs que pilote la remote
        self.ymax=large#largeur du champ et donc y maximum
        self.xmax=long#longueur du champ et donc x maximum
        self.vmax=vmax#vitesse maximale des moteurs
        self.Pos=[]#variable qui va acceuillir les positions atteignables du champ
    
    
    def redim(self, x, y):
        #fonction pour redimensionner son champs et recalculer la matrice position associée
        self.xmax=x
        self.ymax=y
        self.positions()
    
    def positions(self):
        #calcul de la matrice de position du champ
        print("calcul des positions de votre champ \n")
        psize=0.95
        xsize=int(self.xmax//psize)
        ysize=int(self.ymax//psize)
        size=xsize*ysize
        Pos=[[0,0]]*size
        c=0
        for i in range (0,ysize):#on subdivise le champ à l'aide des dimensions d'une photo
            for j in range (0, xsize):
                Pos[c]=[0.475+i*psize, 0.475+j*psize]
                c=c+1
        print("Fait! \n")
        print(Pos)
        self.Pos=Pos
        
   
    def parcour(self):
        #fonction qui lance le parcours automatique de la plateforme mobile
        TOUR=[0,0,0,0]
        for j in range (4):#pilotage de chacun des moteurs
            TOUR[j]=self.Motors[j].pos
        Mot=calcul_pos_mot(self.Pos,self.xmax,self.ymax,TOUR)
        Vit=interpol(Mot)
        for i in range (len(Vit)):
            #self.v=0 #consigne de vitesse
            #self.T #constante de temsp
            #self.etat = False #indicateur de l'état du moteur 
            #self.go=False #le moteur doit fonctionner si go=True
            
            T=Vit[i][4]
            print("T=",T,"\n")
            #moteur 1
            self.Motors[0].v=Vit[i][0]
            self.Motors[0].T=T
            
            #moteur 2
            self.Motors[1].v=Vit[i][1]
            self.Motors[1].T=T
            
            #moteur 3
            self.Motors[2].v=Vit[i][2]
            self.Motors[2].T=T
            
            #moteur 4
            self.Motors[3].v=Vit[i][3]
            self.Motors[3].T=T
            
            for k in range(4):
                while (self.Motors[k]==False):
                    self.Motors[k].etat=True
                while(self.Motors[k].go==False): 
                    self.Motors[k].go=True
            STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
            TEST=[True,True,True,True]
            while (STATE!=TEST):
                STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
                pause(0.1)
            self.where()
            
        print("Un tour a été effectué \n")

    def movemot(self, x, y):
        if x>self.xmax or y>self.ymax: #On verifie que la position est atteignable
            raise ValueError('Value out of bonds \n')
        TOUR=[0,0,0,0]
        L=[(x,y)]
        for j in range (4):
            TOUR[j]=self.Motors[j].pos
        Mot=calcul_pos_mot(L,self.xmax,self.ymax,TOUR)
        Vit=interpol(Mot)
        
        for i in range (len(Vit)):
            #self.v=0 #consigne de vitesse
            #self.T #constante de temsp
            #self.etat = False #indicateur de l'état du moteur 
            #self.go=False #le moteur doit fonctionner si go=True
            
            T=Vit[i][4]
            print("T=",T,"\n")
            #moteur 1
            self.Motors[0].v=Vit[i][0]
            self.Motors[0].T=T
            
            #moteur 2
            self.Motors[1].v=Vit[i][1]
            self.Motors[1].T=T
            
            #moteur 3
            self.Motors[2].v=Vit[i][2]
            self.Motors[2].T=T
            
            #moteur 4
            self.Motors[3].v=Vit[i][3]
            self.Motors[3].T=T
            
            for k in range(4):
                while (self.Motors[k]==False):
                    self.Motors[k].etat=True
                while(self.Motors[k].go==False): 
                    self.Motors[k].go=True
            STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
            TEST=[True,True,True,True]
            while (STATE!=TEST):
                STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
                pause(0.1)
            
        print("Moteur deplacé \n")
        self.where()
        
    def where(self):
        l1=self.Motors[0].pos*0.25
        l2=self.Motors[1].pos*0.25
        print("l1:",l1,"\n l2:",l2,"\n")
        
        x=(l1**2-l2**2+self.xmax**2)/(2*self.xmax)
        print("x: ",x,"\n")
        y=mp.sqrt(l1**2-x**2)
        
        print("la plateforme est en (",x,y,")\n")


class CamBot:
    def __init__ (self, name, Remote, Cam, Doc):
        #pour simplifier le code cela sera l'interface client 
        #de tel sorte que cela soit plus intuitif pour lui
        # Tous ses ordres passent par le même objet
        self.name=name #nom de la caméra
        self.Remote=Remote#télecomande des moteurs du système
        self.cam=Cam#caméra de la plateforme mobile
        self.Doc#Dossier dans lequel seront stocké les photos prises
        
    def moveto(self, x, y):
        self.Remote.movemot(x,y)
    
    def getpic(n):
        print(n+"photo.s prise.s \n")
        
    def recup():
        print("photos envoyées \n")


class Cam:
    
    #classe de la caméra qui fera les fonctions de base de celle-ci
    def __init__(self):
        self.cam #objet qui servira à attacher la caméra
        self.picture #Nombre de photo que la caméra a déja prise

class FakeMotor(th.Thread):
    def __init__(self, serial, vmax, cmax, identifiant):
        th.Thread.__init__(self)
        self.serial = serial #numéro de série
        self.vmax = vmax #vitesse max
        self.cmax = cmax #courant max
        self.id = identifiant #numéro d'id du moteur
        #self.odrv #futur objet qui accrochera le moteur odrive
        self.pos=0 #nombre de tour que le moteur a fait
        self.v=0 #consigne de vitesse
        self.T=0 #constante de temsp
        self.etat = False #indicateur de l'état du moteur 
        self.go=False #le moteur doit fonctionner si go=True
        self.on=True #moteur allumé
    
    def run(self):
        #initialisation des moteurs attention prends du temps (30sec)
        #self.odrv=odrive.find_any(self.serial)#attache du moteur
        #ax = self.odrv.axis0
        #ax.motor.config.pole_pairs = True
        #self.odrv.config.dc_bus_overvoltage_trip_level = 40
        #self.odrv.config.dc_max_positive_current = self.cmax#courant max
        #ax.controller.config.vel_limit = self.vmax#vitesse max
        #self.odrv.config.dc_max_negative_current = -1
        #self.odrv.config.brake_resistor0.resistance = 2
        #self.odrv.config.brake_resistor0.enable = True
        #ax.config.motor.motor_type = od.MotorType.HIGH_CURRENT
        #ax.config.motor.pole_pairs = 7
        #ax.config.motor.torque_constant = 8.27 / 150
        #ax.requested_state = od.AxisState.MOTOR_CALIBRATION #calibration des axes qui prends un certains temps
        #pause(10)
        #self.odrv.inc_encoder0.config.cpr = 8192
        #self.odrv.inc_encoder0.config.enabled = True
        #ax.requested_state = od.AxisState.ENCODER_INDEX_SEARCH #création de l'index de notre encodeur
        #pause(10)
        #ax.requested_state = od.AxisState.ENCODER_OFFSET_CALIBRATION#calcul de l'offset de l'encodeur
        #pause(10)
        #self.odrv.save_configuration()#sauvegarde de la config pour na pas avoir à la refaire après
        
        print("Initialisation \n")
        pause(10)

        #démarer la closed loop de contrôle
        #ax=self.odrv.axis0
        #ax.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
       
        #fonction pour se déplacer à un point de coordonnées x,y
  
        while (self.on==True):
            if (self.go==False):
                #self.odrv.axis0.controller.input_vel = 0
                self.v=0
            if (self.go==True):
                self.etat=True
                #self.odrv.axis0.controller.input_vel =self.v
                print("je vais à la vitesse ",self.v,"\n")
                self.pos=self.pos+(self.v*self.T)
                pause(self.T)
                self.odrv.axis0.controller.input_vel = 0
                self.pos=self.pos+(self.v*self.T)
                #print(self.id,": j'ai désormais fais ",self.pos,"tours \n")
                self.go=False
            self.etat=False
        #implémenter une fonction qui attends que tous les moteurs soient avec un flag GO
        #puis qui fait tourner le moteur à la vitesse v pendant T secondes 
        #puis elle envoie un flag "fait"
        #et elle se remet en standby
        print("Moteur éteint au revoir ! \n")
        return
vmax=20
cmax=10
Mot=[]
for i in range(4):
    m=FakeMotor(100*i,vmax,cmax,i)
    Mot.append(m)

Remote=RemoteMotor(Mot, 50, 50, vmax)

for i in range(4):
    Mot[i].start()
    
d=1
while(d==1):
    c=int(input("Choix du mode: \n 1- parcours \n 2-pilotage \n 3-arrêter \n"))
    if (c==1):
        print("lancement du parcours \n")
        Remote.parcour()
    elif(c==2):
        x=int(input(("Position en x? \n")))
        y=int(input(("Position en y? \n")))
        
        Remote.movemot(x, y)
    else:
        d=0

    

