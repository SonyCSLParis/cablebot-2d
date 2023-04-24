# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:01:21 2023

@author: angab
"""

import AntenneT as ant
import time

print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier!")
test=int(input("Continuer? \n 1- Oui \n 0- Non \n"))
if test==0:
    exit()

host1 = 'localhost'
port1 = 15555

#192.168.1.141
#hoste2 = input("quelle est l'adresse ip de la deuxième antenne? \n")
host2 = 'localhost'
port2 = 15556

host3 = 'localhost'
port3 = 15557

host4 = 'localhost'
port4 = 15558

try:
    #Création des éméteurs
    emet1=ant.EmmeteurT(host1, port1,0)
    emet2=ant.EmmeteurT(host2, port2,12)
    emet3=ant.EmmeteurT(host3, port3,17)
    emet4=ant.EmmeteurT(host4, port4,12)
    EMET=[emet1,emet2,emet3,emet4]
    
    #Création de la cable bot
    cable=ant.Cablebot(EMET, 5, 5, 1)
    
    #démarage du robot
    cable.start()
    
    a=1
    while a==1:
        #CHOIX DES MODES
        
        b=True
        t_compt=0
        while b==True:
            mod1=input("Quel mode moteur 1? \n t = torque \n v = vitesse \n")
            if mod1=='t': 
                t_compt+=1
            mod2=input("Quel mode moteur 2? \n t = torque \n v = vitesse \n")
            if mod2=='t': 
                t_compt+=1
            mod3=input("Quel mode moteur 3? \n t = torque \n v = vitesse \n")
            if mod3=='t': 
                t_compt+=1
            mod4=input("Quel mode moteur 4? \n t = torque \n v = vitesse \n")
            if mod4=='t': 
                t_compt+=1
            if t_compt>=3:
                print('Tous les moteurs ne peuvent pas être en couple! Maximum deux moteurs en couple \n')
            else:
                MODE=[mod1,mod2,mod3,mod4]
                b=False
        
        cable.switch(MODE)
        
        
        #CHOIX DES VALEURS
        #1
        if mod1=='t':
            val1=0.1
        else:
            val1=float(input("Quelle vitesse moteur 1? \n"))
            
        #2
        if mod2=='t':
            val2=0.1
        else:
            val2=float(input("Quelle vitesse moteur 2? \n"))
            
        #3
        if mod3=='t':
            val3=0.1
        else:
            val3=float(input("Quelle vitesse moteur 3? \n"))
            
        #4
        if mod4=='t':
            val4=0.1
        else:
            val4=float(input("Quelle vitesse moteur 4? \n"))
        
        VAL=[val1,val2,val3,val4]
        T=float(input("Pendant quelle durée?\n"))
        
        cable.speed(VAL,T)
        a=int(input("Encore? \n 0-Non \n 1-Oui \n"))
        
        #TEST QUOTIDIEN
        
        print('test du parcours quotidien \n')
        cable.quotidien()
        print("fin du quotidien")
        time.sleep(2)
        cable.end()
    
except BaseException as e:
    time.sleep(2)
    cable.end()
    print("Erreur :", e)