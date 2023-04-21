1# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:37:31 2023

@author: angab
"""
import AntenneT as ant
#import testT as t
import time

print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier!")
test=int(input("Continuer? \n 1- Oui \n 0- Non \n"))
if test==0:
    exit()

#192.168.1.166
hoste = input("quelle est l'adresse ip? \n")
port1 = 15555

emet1=ant.EmmeteurT(hoste, port1,0)

emet1.connect()
time.sleep(20)

mode='v'
T=5
emet1.switch(mode)
emet1.pilote(3, T)
time.sleep(T)
emet1.pilote(-3,T)
time.sleep(T)
emet1.pilote(0,T)
    
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

while nxt==1:
    emet1.switch(mode)
    val=float(input("Quelle vitesse? \n"))
    T=float(input("Pendant quelle durée?\n"))
    emet1.pilote(val,T)
    time.sleep(T)
    
    nxt=int(input("Nouvelle consigne? \n 1 - Oui \n 0- Non \n"))

#emet.resume()
time.sleep(2)
emet1.end()


