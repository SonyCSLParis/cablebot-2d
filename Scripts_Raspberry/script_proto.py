# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:28:53 2023

@author: angab
"""


import math as mp
import test_ligne.py as tes
import odrive 
import time
import odrive.enums as od

def calcul_pos_mot(X, lon, Tour): #à adapter au test en cours en fonction du nombre de moteur utilisés
    Mot=[0,0]
    C1=Tour[0]
    #print("C1", C1)
    C2=Tour[1]
    #print("C2", C2)
    d=0.2
    Conv=0.25 #à definir avant
    #print(x,y)
    l1=X
    #print("l1: ",l1)
    l1=mp.sqrt(l1**2+d**2)
    #plt.plot(i,l1,color='red',marker='x')
    l2=lon-X
    #print("l2", l2)
    l2=mp.sqrt(l2**2+d**2)
    #plt.plot(i,l2,color='green',marker='x')
    t1=(l1/Conv)
    t2=(l2/Conv)
    c1=t1-C1
    c2=t2-C2
    Mot=[c1,c2]
    Tour=[t1,t2]
    return Mot, Tour

def interpol(L):
    vel_max=5
    Vel=[0, 0]
    maxi=L[0]
    V1=0
    V2=0
    #V3=0
    #V4=0
    C=L[1]
    if abs(C)>=maxi:
        maxi=abs(C)
    print("maxi=",maxi)
    T=maxi/vel_max #temps en seconde
    print("T=",T)
    V1=L[0]/T
    V2=L[1]/T
    #V3=C[2]/T
    #V4=C[3]/T
    Vel=[V1, V2,T]
    return Vel

odrv0 = None

try:
    # Recherche d'un ODrive connecté
    odrv0 = odrive.find_any()
    odrv0.axis0.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
    #Mode controle en vitesse
        
    odrv0.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
    Tour=[0,200] #valeur à adpater au test
    for i in range(40): #ici la valeur correspond au  nombre de mètre à faire *4
        Mot=tes.calcul_pos_mot(i/4,10,Tour) #aller verifier que le facteur de conversion tour/longeur est le bon
        V=tes.interpol(Mot)
        odrv0.axis0.controller.input_vel = V[0] #Pour l'autre moteur remplacer le 0 par 1
        while odrv0.axis0.current_state != od.AXIS_STATE_CLOSED_LOOP_CONTROL:
            pass
        time.sleep(V[-1])
        odrv0.axis0.controller.input_vel = 0
        while odrv0.axis0.current_state != od.AXIS_STATE_IDLE:
            pass
    
except BaseException as e:  
    print("Impossible de se connecter à l'ODrive : {}".format(e))


odrv0.axis0.requested_state = od.AXIS_STATE_IDLE