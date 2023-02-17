# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:26:25 2023

@author: angab
"""
import odrive
import odrive.enmus as od
import os 
import cv2 as cv
import time
import math as mp

def pause(t = 0.1):
    """
    pas grand-chose à ajouter...
    """
    print("Pause started")
    time.sleep(t)
    print("Pause ended")
    return None

class Motor:
    def __init__(self, serial, vmax, cmax, identifiant):
        self.serial = serial #numéro de série
        self.vmax = vmax #vitesse max
        self.cmax = cmax #courant max
        self.id = identifiant #numéro d'id du moteur
        self.odrv #futur objet qui accrochera le moteur odrive
        self.pos=0 #nombre de tour que le moteur a fait
        
        # idée créer un self.state=0 si open et 1 si busy
    
    def get(self):
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
        
    def on(self):
       #démarer la closed loop de contrôle
       print("GO")
       ax=self.odrv.axis0
       ax.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
       
    #fonction pour se déplacer à un point de coordonnées x,y
    def moveto(self,v, T):
        self.odrv.axis0.controller.input_vel = v
        pause(T)
        self.odrv.axis0.controller.input_vel = 0
        #implémenter une fonction qui attends que tous les moteurs soient avec un flag GO
        #puis qui fait tourner le moteur à la vitesse v pendant T secondes 
        #puis elle envoie un flag "fait"
        #et elle se remet en standby
        print("fait")
        
        
    def off(self):
        #detacher le moteur et l'éteindre
        print("Bye")
    
    #idée de def status(self): qui renvoit juste le state du moteur pour que l'on sache quand on peut envoyer la commande suivante

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
        for i in range (len(self.Pos)):
            TOUR=[]
            x=self.Pos[0]
            y=self.Pos[1]
            for j in range (4):#pilotage de chacun des moteurs
                TOUR[j]=self.Motors[j].pos
            self.Motors[0].movexy(x, y, TOUR)
            self.Motors[1].movexy(x, y, TOUR)
            self.Motors[2].movexy(x, y, TOUR)
            self.Motors[3].movexy(x, y, TOUR)
        print("Un tour a été effectué \n")

    def movemot(self, x, y):
        if x>self.xmax or y>self.ymax: #On verifie que la position est atteignable
            raise ValueError('Value out of bonds')
        TOUR=[]
        for j in range (4):
            TOUR[j]=self.Motors[j].pos
        self.Motors[0].movexy(x, y, TOUR)
        self.Motors[1].movexy(x, y, TOUR)
        self.Motors[2].movexy(x, y, TOUR)
        self.Motors[3].movexy(x, y, TOUR)


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
        print(n+"photo.s prise.s")
        
    def recup():
        print("photos envoyées")


class Cam:
    
    #classe de la caméra qui fera les fonctions de base de celle-ci
    def __init__(self):
        self.cam #objet qui servira à attacher la caméra
        self.picture #Nombre de photo que la caméra a déja prise