# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:35:48 2023

@author: angab
"""

import Remote_c as rem
import cablebot_c as cab
import Camera_c as cam


print("Programme de test des classes du cable bot, pensez à lancer les simulations de moteur en premier!")
test=int(input("Continuer? \n 1- Oui \n 0- Non"))
if test==0:
    exit()

hoste = "localhost"
port1 = 15555
port2 = 15556
xmax = 5
ymax = 5
path1=input("Indiquez le premier Path")
path2=input("Indiquez le second Path")

if __name__=="__main__":
    Cam1=cam.Fakecam("nono",path1)
    prox1=rem.ProxyMotor(hoste, port1, xmax, ymax)
    prox2=rem.ProxyMotor(hoste, port2, xmax, ymax)
    Proxs=[prox1,prox2]
    Bot=cab.InterfaceBot(Proxs,Cam1,xmax,ymax)
    
    
    Bot.on()
    print("test pilotage")
    Bot.pilotage(2,2)
    
    print("test quotidien")
    Bot.quotidien()
    
    print("test new path")
    Bot.majpath(path2)
    
    print("test raz")
    Bot.zero()
    
    print("test prise de photo")
    Bot.take_pics(5)
    
    print("test fin")
    Bot.end()
    