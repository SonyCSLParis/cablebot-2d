# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:58:14 2023

@author: angab
"""

import AntenneT as ant
#import testT as t
import time

print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier! \n ordre: Nord, Ouest, Est, Sud")
input("Continuer?")

#192.168.1.166
#hoste1 = input("quelle est l'adresse ip de la première antenne? \n")
#hostenord = '192.168.1.130'
hostenord = 'localhost'
portnord = 15555

#192.168.1.141
#hoste2 = input("quelle est l'adresse ip de la deuxième antenne? \n")
hosteouest = '192.168.1.141'
#hosteouest = 'localhost'
portouest = 15556

#hosteest = '192.168.1.102'
hosteest = 'localhost'
portest = 15557

hostesud = '192.168.1.150'
#hostesud = 'localhost'
portsud = 15558

hostcam='192.168.1.184'
portcam = 15559

try:
    #Création des éméteurs
    emet1=ant.EmmeteurT(hostenord,portnord,0)
    emet2=ant.EmmeteurT(hosteouest,portouest,0)
    emet3=ant.EmmeteurT(hostesud,portsud,0)
    emet4=ant.EmmeteurT(hosteest,portest,0)
    EMET=[emet1,emet2,emet3,emet4]
    
    #Création de la caméra 
    cam = ant.EmmetCam(hostcam, portcam)
    #cam = None
    #Création de la cable bot
    cable=ant.Cablebot(cam,EMET, 3, 3, 1)
    
    #démarage du robot
    cable.start()
    x=1
    tor1=-0.1
    tor2=-0.1
    tor3=-0.1
    tor4=-0.1
    #test contrôle manuelle
            #Choix des modes
    b=True
    while b==True:
            
        #Au cas où on trouve les couples trop ou pas assez elevez on peut les mettre à jours
        change=input("Mettre à jour les couples des moteurs? \n o- oui \n n- non \n")
        if change=='o':
            tor1=float(input("Couple du moteur Nord?\n"))
            tor2=float(input("Couple du moteur Ouest?\n"))
            tor3=float(input("Couple du moteur Sud?\n"))
            tor4=float(input("Couple du moteur Est?\n"))
            TOR=[tor1,tor2,tor3,tor4]
            cable.set_torques(TOR)
            
            #choix du mode de pilotage des moteurs
        mod1=input("Quel mode moteur Nord? \n t = torque \n v = vitesse \n")
        mod2=input("Quel mode moteur Ouest? \n t = torque \n v = vitesse \n")
        mod3=input("Quel mode moteur Sud? \n t = torque \n v = vitesse \n")
        mod4=input("Quel mode moteur Est? \n t = torque \n v = vitesse \n")
        if mod1=='v' and mod3=='v':
            print ('impossible')
        elif mod2=='v' and mod4=='v':
            print('impossible')
        else:
            b=False
        
        cable.switch([mod1,mod2,mod3,mod4])
        
        #Choix des valeurs
        if mod1=='t':
            val1=tor1
        else:
            val1=float(input("Quelle vitesse moteur Nord? \n"))
           
        if mod2=='t':
            val2=tor2
        else:
            val2=float(input("Quelle vitesse moteur Ouest? \n"))
            
            
        if mod3=='t':
            val3=tor3
        else:
            val3=float(input("Quelle vitesse moteur Sud? \n"))
                
        if mod4=='t':
            val4=tor4
        else:
            val4=float(input("Quelle vitesse moteur Est? \n"))
        V=[val1,val2,val3,val4]
            
        #choix de la durée d'action
        T=float(input("Pendant quelle durée?\n"))
            
            
        cable.pilote(V,T)
        pic=int(input("Photo? \n 1-oui \n 0-Non"))
        if pic==1:
            cable.takepic()
        b=int(input("Encore? \n 0-Non \n 1-Oui \n"))
    
    parc=int(input("Parcours?\n 0-Non \n 1-Oui"))
    if parc==1:
        cable.quotidien()
    cable.endrun()       
    cable.end()
except BaseException as e:
    time.sleep(2)
    cable.end()
    print("Erreur :", e)

