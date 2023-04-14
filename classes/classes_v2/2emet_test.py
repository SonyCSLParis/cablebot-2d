# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:58:14 2023

@author: angab
"""

import AntenneT as ant
#import testT as t
import time

print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier!")
test=int(input("Continuer? \n 1- Oui \n 0- Non \n"))
if test==0:
    exit()

#192.168.1.102
hoste1 = input("quelle est l'adresse ip de la première antenne? \n")
port1 = 15555

#192.168.1.141
hoste2 = input("quelle est l'adresse ip de la deuxième antenne? \n")
port2 = 15556


#Création des éméteurs
emet1=ant.EmmeteurT(hoste1, port1)
emet2=ant.EmmeteurT(hoste2, port2)
EMET=[emet1,emet2]


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



"""
Pos=t.pos_lig()
Tour=[0,8]
for i in range(len(Pos)):
    L=t.calcul_pos_mot_ligne(Pos)
    Mot=t.calc_tour_ligne(L,Tour)
    
print("len MOT: ",len(Mot))
for i in range (len(Mot)):
    print("Mot: ",Mot[i][0])
    if (Mot[i][0]<=-100):
        mode='t'
        val=0.08
        T=2
    else:
        mode='v'
        T=t.calc_t(Mot[i][0])
        print("T=",T)
        val=t.calc_vit(T,Mot[i][0])
    
    emet.pilote(val, T, mode)
    time.sleep(T+1)
"""
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
    nxt=input("Nouvelle consigne? \n 1 - Oui \n 0- Non \n")

#emet.resume()

#Fin de programme
time.sleep(2)
emet1.end()