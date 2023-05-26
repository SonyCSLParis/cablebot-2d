# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:55:45 2023

@author: angab
"""

import time
import keyboard



import AntenneT as ant


print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier! \n ordre: Nord, Ouest, Sud, Est")
input("Continuer?")

#192.168.1.166 ip de leonard
#hoste1 = input("quelle est l'adresse ip de la première antenne? \n")
hostenord = '192.168.1.130'
#hostenord = 'localhost'
portnord = 15555

#192.168.1.141
#hoste2 = input("quelle est l'adresse ip de la deuxième antenne? \n")
hosteouest = '192.168.1.141'
#hosteouest = 'localhost'
portouest = 15556

hostesud = '192.168.1.150'
#hostesud = 'localhost'
portsud = 15557

hosteest = '192.168.1.102'
#hosteest = 'localhost'
portest = 15558


hostcam='192.168.1.184'
portcam = 15559

try:
    #Création des éméteurs
    emet1=ant.EmmeteurT(hostenord,portnord,0)
    emet2=ant.EmmeteurT(hosteouest,portouest,0)
    emet3=ant.EmmeteurT(hosteest,portest,0)
    emet4=ant.EmmeteurT(hostesud,portsud,0)
    EMET=[emet1,emet2,emet3,emet4]
    
    #Création de la caméra 
    #cam = ant.EmmetCam(hostcam, portcam)
    cam = None
    #Création de la cable bot
    cable=ant.Cablebot(cam,EMET, 3, 3, 1)
    
    #démarage du robot
    cable.start()
    
    #TENDRE LES CABLES
    Mod=['v','v','v','v']
    cable.switch(Mod)
    tend=1
    while tend==1:   
        V=[-1,-1,-1,-1]
        T=1
        cable.pilote(V,T)
        tend=int(input("Encore? \n 1-Oui \n 0-Non \n"))
    
    #Tendre un seul câble
    solocable=1
    while solocable==1:
        who=input("tendre quel câble? \n n-nord \n o-ouest \n s-sud \n e-est \n")
        if who=='n' or who=='N':
            Mod=['t','v','v','v','v']
        elif who=='o' or who=='O':
            Mod=['v','t','v','v']
        elif who=='s' or who=='S':
            Mod=['v','v','t','v']
        elif who=='e'or who=='E':
            Mod=['v','v','v','t']
        else:
            Mod=['v','v','v','v']
        cable.switch(Mod)
        solocable=int(input("Encore? \n 1-Oui \n"))
    
    manu=int(input("Passer en mode manuel? \n 1-oui \n"))
    if manu==1:
        TOR=[-0.1,-0.1,-0.1,-0.1]
        cable.set_torques(TOR)
        while True:
            v=-1
            if keyboard.is_pressed('space'):
                print("Fin de pilotage")
                break
            if keyboard.is_pressed('up'):
                print('vers le haut')
                Mod=['t','v','v','t']
                cable.switch(Mod)
                V=[v,v,v,v]
                cable.pilote(V, T)
                time.sleep(T)
            if keyboard.is_pressed('right'):
                print('vers la droite')
                Mod=['v','v','t','t']
                cable.switch(Mod)
                V=[v,v,v,v]
                cable.pilote(V, T)
                time.sleep(T)
            if keyboard.is_pressed('left'):
                print('vers la gauche')
                Mod=['t','t','v','v']
                cable.switch(Mod)
                V=[v,v,v,v]
                cable.pilote(V, T)
                time.sleep(T)
            if keyboard.is_pressed('down'):
                print('vers le bas')
                Mod=['v','t','t','v']
                cable.switch(Mod)
                V=[v,v,v,v]
                cable.pilote(V, T)
                time.sleep(T)

    print("Mode automatique du carré\n Vérifiez que vous êtes bien en 0,0")
    input("pause, cliquez quand prêt")
    #Etape 1
    print("Etape 1")
    T=5
    v=-3
    Mod=['t','t','t','v']
    V=[v,v,v,v]
    cable.switch(Mod)
    cable.pilote(V,T)
    time.sleep(T)
    
    #Etape 2
    print("Etape 2")
    T=5
    v=-3
    Mod=['t','t','v','t']
    V=[v,v,v,v]
    cable.switch(Mod)
    cable.pilote(V,T)
    time.sleep(T)
    
    #Etape 3:*
    print("Etape 3")
    T=5
    v=-3
    Mod=['t','v','t','t']
    V=[v,v,v,v]
    cable.switch(Mod)
    cable.pilote(V,T)
    time.sleep(T)
    
    #Etape 4
    print("Etape 4")
    T=5
    v=-3
    Mod=['v','t','t','t']
    V=[v,v,v,v]
    cable.switch(Mod)
    cable.pilote(V,T)
    time.sleep(T)
    
    #Etape 5
    print("Etape 5")
    T=3
    v=-3
    Mod=['t','t','v','t']
    V=[v,v,v,v]
    cable.switch(Mod)
    cable.pilote(V,T)
    time.sleep(T)
    
    cable.end()
    
except BaseException as e:
    time.sleep(2)
    cable.end()
    print("Erreur :", e)