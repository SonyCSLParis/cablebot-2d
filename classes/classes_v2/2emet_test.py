# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:58:14 2023

@author: angab
"""

import AntenneT as ant
#import testT as t
import time

print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier!")
input("Continuer?")

#192.168.1.166
#hoste1 = input("quelle est l'adresse ip de la première antenne? \n")
hoste1 = '192.168.1.102'
port1 = 15555

#192.168.1.141
#hoste2 = input("quelle est l'adresse ip de la deuxième antenne? \n")
hoste2 = '192.168.1.141'
port2 = 15556

hostcam='192.168.1.184'
portcam = 15557

try:
    #Création des éméteurs
    emet1=ant.EmmeteurT(hoste1, port1,5)
    emet2=ant.EmmeteurT(hoste2, port2,5)
    EMET=[emet1,emet2]
    
    #Création de la caméra 
    cam = ant.EmmetCam(hostcam, portcam)
    
    #Création de la cable bot
    cable=ant.Cablebot(cam,EMET, 5, 5, 1)
    
    #démarage du robot
    cable.start()
    x=1
    tor1=-0.18
    tor2=-0.18
    while x==1:
    #test contrôle manuelle
        a=1
        while a==1:
            #Choix des modes
            b=True
            while b==True:
            
                #Au cas où on trouve les couples trop ou pas assez elevez on peut les mettre à jours
                change=input("Mettre à jour les couples des moteurs? \n o- oui \n n- non \n")
                if change=='o':
                    tor1=float(input("Couple du moteur 1?\n"))
                    tor2=float(input("Couple du moteur 2?\n"))
                    TOR=[tor1,tor2]
                    cable.set_torques(TOR)
            
                #choix du mode de pilotage des moteurs
                mod1=input("Quel mode moteur 1? \n t = torque \n v = vitesse \n")
                mod2=input("Quel mode moteur 2? \n t = torque \n v = vitesse \n")
                if mod1=='t' and mod2=='t':
                    print ('impossible de mettre les deux moteurs en couple')
                else:
                    b=False
        
            cable.switch([mod1,mod2])
        
            #Choix des valeurs
            if mod1=='t':
                val1=tor1
            else:
                val1=float(input("Quelle vitesse moteur 1? \n"))
            if mod2=='t':
                val2=tor2
            else:
                val2=float(input("Quelle vitesse moteur 2? \n"))
            T=float(input("Pendant quelle durée?\n"))
            V=[val1,val2]
        
            cable.pilote(V,T)
            a=int(input("Encore? \n 0-Non \n 1-Oui \n"))
        
        
        #test autonome de la ligne
        ligne=int(input("Voulez-vous tester la ligne seul maintenant? \n 0-Non \n 1-Oui \n"))
        while ligne==1:
            cable.line_test()
            time.sleep(2)
            ligne=int(input("Encore? \n 1-oui \n 0-non \n"))
        x=int(input("Repasser en mode manuel ou terminer? \n 1- mode manuel \n 2- fin \n"))
    cable.end()
except BaseException as e:
    time.sleep(2)
    cable.end()
    print("Erreur :", e)
            
                
            
"""
Programme sans le cable bot, fonctionnel et qui pilote deux moteurs à distance simultanément
"""
"""
 #Connexion aux moteurs
for i in EMET:
    i.connect()
time.sleep(20)
mode='v'
T=5

#Pilotage automatique
for i in EMET:
    i.switch(mode)
time.sleep(1)

for i in EMET:
    i.pilote(3,T)
time.sleep(T)

for i in EMET:
    i.pilote(-3,T)
time.sleep(T)

for i in EMET:
    i.pilote(0,0)

nxt=int(input("Voulez vous passer à la phase manuelle? \n 0-Non \n 1-Oui \n"))

#On s'assure d'être en mode vitesse
for i in EMET:
    i.switch(mode)

while nxt==1:
    #choix des vitesses
    val1=float(input("Quelle vitesse moteur 1? \n"))
    val2=float(input("Quelle vitesse moteur 2? \n"))
    T=float(input("Pendant quelle durée?\n"))
    
    #Pilotage
    emet1.pilote(val1,T)
    emet2.pilote(val2,T)
    time.sleep(T)
    
    #Condition de sortie
    nxt=int(input("Nouvelle consigne? \n 1 - Oui \n 0- Non \n"))

#emet.resume()

#Fin de programme
time.sleep(2)
emet1.end()
emet2.end()
"""

