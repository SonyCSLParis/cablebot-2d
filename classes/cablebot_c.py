# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:19:08 2023

@author: angab
"""

import moteur as fct
import time

def pause(t):
    time.sleep(t)

class InterfaceBot:
    def __init__(self, Proxys, camera, xmax, ymax):
        self.Proxs=Proxys
        self.xmax=xmax
        self.ymax=ymax
        self.Pos=fct.calcul_pos(xmax,ymax)
        self.cam=camera
    
    
    def on(self):
        for prox in self.Proxs:
            prox.connect(0)
        test=self.cam.on()
        if test:
            print("prêt à l'emplois")
        else:
            print("echec dans l'allumage")
        
    def pilotage(self,x,y):
        Tour=[]
        for prox in self.Proxs:
            Tour.append(prox.tour)
        Mot=fct.calcul_pos_mot([x,y],self.xmax,self.ymax,Tour)
        Vit=fct.interpol(Mot)
        i=0
        T=Vit[-1]
        print("T: ",T)
        for prox in self.Proxs:
            prox.pilote(Vit[i],T)
            i=i+1
        pause(T)
        
    def quotidien(self):
        i=0
        for pos in self.Pos:
            x=pos[0]
            y=pos[1]
            self.pilotage(x,y)
            test=self.cam.takepic()
            if test:
                print("photo ",str(i)," prise")
            else:
                print("erreur prise de photo")
                return False
            i=i+1

    def take_pics(self,n):
        for i in range(n):
            self.cam.takepic()
    
    def zero(self):
        self.cam.raz()
        print("photo remise à jour")

    
    def end(self):
        for prox in self.Proxs:
            prox.end()
            pause(1)

