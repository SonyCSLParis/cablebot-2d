# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:55:45 2023

@author: angab
"""

import time
import travel
import AntenneT as ant


print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier! \n ordre: Nord, Ouest, Sud, Est")
input("Continuer?")

#192.168.1.166 ip de leonard
hostenord = '192.168.1.128'
#hostenord = 'localhost'
portnord = 15555

#192.168.1.141
hosteouest = '192.168.1.141'
#hosteouest = 'localhost'
portouest = 15555

hosteest = '192.168.1.102'
#hosteest = 'localhost'
portest = 15555

hostesud = '192.168.1.150'
#hostesud = 'localhost'
portsud = 15555



hostcam='192.168.1.184'
portcam = 15555

try:
    #Création des éméteurs
    emet1=ant.EmmeteurT(hosteouest,portouest,0)
    emet2=ant.EmmeteurT(hostesud,portsud,0)
    emet3=ant.EmmeteurT(hostenord,portnord,0)
    emet4=ant.EmmeteurT(hosteest,portest,0)
    EMET=[emet1,emet2,emet3,emet4]
    
    #Création de la caméra 
    #cam = ant.EmmetCam(hostcam, portcam)
    cam = None
    #Création de la cable bot
    cable=ant.Cablebot(cam,EMET, 3, 3, 1)
    
    #démarage du robot
    cable.start()
    cable.speed([0,0,0,0])
    input("ready?")
    
    #Tension des câbles
    print("On tend les câbles")
    Tor=[-0.1,-0.1,-0.1,-0.1]
    cable.set_torques(Tor)
    time.sleep(2)
    for i in range(4):
        Mod=['v','v','v','v']
        Mod[i]='t'
        cable.switch(Mod)
        time.sleep(2)
    
    input("next?")
    
    #Test des couples
    print("Deplacement à la main")
    mod=['t','t','t','t']
    cable.switch(mod)
    
    a=1
    while a==1:
        dep=int(input("Deplacement? \n 1-oui "))
        while dep==1:
            #Position de départ
            xs=float(input("Quel x de départ? \n"))
            ys=float(input("Quel y de départ? \n"))
    
            #Position d'arrivée
            xg=float(input("Quel x d'arrivé? \n"))
            yg=float(input("Quel y d'arrivé? \n"))
    
            S=[xs,ys]
            G=[xg,yg]
    
            #Temps de trajet
            T=int(input("Quelle durée? \n"))
    
            cable.travel(S,G,T)
            print("fin de parcours")
            input("Deplacement à la main")
            mod=['t','t','t','t']
            cable.switch(mod)
            dep=int(input("Point suivant? \n 1-Oui \n 0-Non"))
        pic=int(input("Prendre une photo? \n 1-Oui \n"))
        if pic==1:
            cable.takepic()
        a=int(input("Bouger à nouveau? \n 1-oui"))
    
    input("Fin de parcours")
    cable.end()
   
    
except BaseException as e:
    time.sleep(2)
    cable.end()
    print("Erreur :", e)