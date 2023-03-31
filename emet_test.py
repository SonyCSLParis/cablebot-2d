# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:37:31 2023

@author: angab
"""
import AntenneT as ant
import testT as t
import time

print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier!")
test=int(input("Continuer? \n 1- Oui \n 0- Non \n"))
if test==0:
    exit()

hoste = "localhost"
port1 = 15555

emet=ant.EmmeteurT(hoste, port1)

emet.connect()
Pos=t.calcul_pos(5,5,1)
Tour=[0,25,25,35]
Cons=[]
Tor=[]
for i in range(len(Pos)):
    cons, Tour, tor =t.calcul_pos_mot(Pos[i],5,5, Tour)
    Cons.append(cons[0])
    Tor.append(tor[0])

for i in range (len(Pos)):
    if (Cons[i]<0):
        mode='t'
        val=Tor[i]
    else:
        mode='v'
        T=t.calc_t(Cons[i])
        print(T)
        val=t.calc_vit(T,Cons[i])
    
    emet.pilote(val, T, mode)

emet.resume()
time.sleep(2)
emet.end()


