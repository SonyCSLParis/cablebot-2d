# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:25:56 2023

@author: angab
"""

import time
import math as mp
import threading as th

def pause(t = 0.1):
    """
    pas grand-chose à ajouter...
    """
    #print("Pause started")
    time.sleep(t)
    #print("Pause ended")
    return None

def calcul_pos_mot(L, lon, lar, Tour):
     Mot=[[0,0,0,0]]*len(L)
     Lon=[[0,0,0,0]]*len(L)
     k1=Tour[0]
     k2=Tour[1]
     k3=Tour[2]
     k4=Tour[3]
     for i in range (len(L)):
         y=L[i][0]
         x=L[i][1]
         Conv=1
         #print(x,y)
         l1=mp.sqrt(x**2+y**2)
         #l1=mp.sqrt(l1**2+d**2)
         #plt.plot(i,l1,color='red',marker='x')
         l2=mp.sqrt((lon-x)**2+y**2)
         #l2=mp.sqrt(l2**2+d**2)
         #plt.plot(i,l2,color='green',marker='x')
         l3=mp.sqrt(x**2+(lar-y)**2)
         #l3=mp.sqrt(l3**2+d**2)
         #plt.plot(i,l3,color='blue',marker='x')
         l4=mp.sqrt((lon-x)**2+(lar-y)**2)
         #l4=mp.sqrt(l4**2+d**2)
         #plt.plot(i,l4,color='yellow',marker='x')
         Lon[i]=[l1,l2,l3,l4]
         #0,5 à changer car juste le rapport de m.tour-1
         c1=(l1/Conv)-k1
         c2=(l2/Conv)-k2
         c3=(l3/Conv)-k3
         c4=(l4/Conv)-k4
         k1=l1/Conv
         k2=l2/Conv
         k3=l3/Conv
         k4=l4/Conv
         Mot[i]=[c1,c2,c3,c4]
     return Mot

 #interpolatoin via les vitesses de chaque moteur et une constante de temps
def interpol(L):
     vel_max=10
     Vel=[[0, 0, 0, 0]]*len(L)
     for i in range(len(L)):
         V1=0
         V2=0
         V3=0
         V4=0
         C=L[i]
         maxi=abs(C[0])
         for j in C:
             if abs(j)>=maxi:
                 maxi=abs(j)
         T=maxi/vel_max #temps en seconde
         V1=C[0]/T
         V2=C[1]/T
         V3=C[2]/T
         V4=C[3]/T
         Vel[i]=[V1, V2, V3, V4,int(T)]
     return Vel
 
    
class FakeMotor(th.Thread):
    def __init__(self, serial, vmax, cmax, identifiant):
        th.Thread.__init__(self)
        self.serial = serial #numéro de série
        self.vmax = vmax #vitesse max
        self.cmax = cmax #courant max
        self.id = identifiant #numéro d'id du moteur
        #self.odrv #futur objet qui accrochera le moteur odrive
        self.pos=0 #nombre de tour que le moteur a fait
        self.v=0 #consigne de vitesse
        self.T=0 #constante de temsp
        self.etat = False #indicateur de l'état du moteur 
        self.go=False #le moteur doit fonctionner si go=True
        self.on=True #moteur allumé
    
    
    def run(self):
        while (self.on==True):
            if (self.go==False):
                self.v=0
            if (self.go==True):
                self.etat=True
                print(self.id,": je vais à la vitesse ",self.v,"tours.sec-1 \n")
                self.pos=self.pos+(self.v*self.T)
                pause(self.T)
                self.pos=self.pos+(self.v*self.T)
                print(self.id,": j'ai désormais fais ",self.pos,"tours \n")
                self.go=False
            self.etat=False
        
        print("Moteur éteint au revoir ! \n")
        return


class RemoteMotor:
    
    def __init__(self, Motors, large, long, vmax):
        self.Motors=Motors#listes des moteurs que pilote la remote
        self.ymax=large#largeur du champ et donc y maximum
        self.xmax=long#longueur du champ et donc x maximum
        self.vmax=vmax#vitesse maximale des moteurs
        self.Pos=[]#variable qui va acceuillir les positions atteignables du champ
    
    
    def redim(self, x, y):
        #fonction pour redimensionner son champs et recalculer la matrice position associée
        self.xmax=x
        self.ymax=y
        self.positions()
    
    def positions(self):
        #calcul de la matrice de position du champ
        print("calcul des positions de votre champ \n")
        psize=0.95
        xsize=int(self.xmax//psize)
        ysize=int(self.ymax//psize)
        size=xsize*ysize
        Pos=[[0,0]]*size
        c=0
        for i in range (0,ysize):#on subdivise le champ à l'aide des dimensions d'une photo
            for j in range (0, xsize):
                Pos[c]=[0.475+i*psize, 0.475+j*psize]
                c=c+1
        print("Fait! \n")
        #print(Pos)
        self.Pos=Pos
        
   
    def parcour(self):
        #fonction qui lance le parcours automatique de la plateforme mobile
        TOUR=[0,0,0,0]
        for j in range (4):#pilotage de chacun des moteurs
            TOUR[j]=self.Motors[j].pos
        Mot=calcul_pos_mot(self.Pos,self.xmax,self.ymax,TOUR)
        Vit=interpol(Mot)
        for i in range (len(Vit)):
            #self.v=0 #consigne de vitesse
            #self.T #constante de temsp
            #self.etat = False #indicateur de l'état du moteur 
            #self.go=False #le moteur doit fonctionner si go=True
            
            T=Vit[i][4]
            print("T=",T,"\n")
            #moteur 1
            self.Motors[0].v=Vit[i][0]
            self.Motors[0].T=T
            
            #moteur 2
            self.Motors[1].v=Vit[i][1]
            self.Motors[1].T=T
            
            #moteur 3
            self.Motors[2].v=Vit[i][2]
            self.Motors[2].T=T
            
            #moteur 4
            self.Motors[3].v=Vit[i][3]
            self.Motors[3].T=T
            
            for k in range(4):
                while(self.Motors[k].etat==False):
                    self.Motors[k].etat=True
                while(self.Motors[k].go==False): 
                    self.Motors[k].go=True
            STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
            TEST=[True,True,True,True]
            while (STATE!=TEST):
                STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
                pause(0.1)
            self.where()
            
        print("Un tour a été effectué \n")

    def movemot(self, x, y):
        if x>self.xmax or y>self.ymax: #On verifie que la position est atteignable
            raise ValueError('Value out of bonds \n')
        TOUR=[0,0,0,0]
        L=[(x,y)]
        for j in range (4):
            TOUR[j]=self.Motors[j].pos
        print("Tour: ",TOUR, "\n")
        Mot=calcul_pos_mot(L,self.xmax,self.ymax,TOUR)
        Vit=interpol(Mot)
        
        for i in range (len(Vit)):
            #self.v=0 #consigne de vitesse
            #self.T #constante de temsp
            #self.etat = False #indicateur de l'état du moteur 
            #self.go=False #le moteur doit fonctionner si go=True
            
            T=Vit[i][4]
            print("T=",T,"\n")
            #moteur 1
            self.Motors[0].v=Vit[i][0]
            self.Motors[0].T=T
            
            #moteur 2
            self.Motors[1].v=Vit[i][1]
            self.Motors[1].T=T
            
            #moteur 3
            self.Motors[2].v=Vit[i][2]
            self.Motors[2].T=T
            
            #moteur 4
            self.Motors[3].v=Vit[i][3]
            self.Motors[3].T=T
            
            for k in range(4):
                while (self.Motors[k]==False):
                    self.Motors[k].etat=True
                while(self.Motors[k].go==False): 
                    self.Motors[k].go=True
            STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
            TEST=[True,True,True,True]
            while (STATE!=TEST):
                STATE=[self.Motors[0].etat,self.Motors[1].etat,self.Motors[2].etat,self.Motors[3].etat]
                pause(0.1)
            
        print("Moteur deplacé \n")
        self.where()

    def where(self):
        l1=self.Motors[0].pos
        l2=self.Motors[1].pos
        l3=self.Motors[2].pos
        l4=self.Motors[3].pos
        c=self.xmax
        l=self.ymax
        x = (l1**2 - l2**2 + c**2) / (2*c)
        y = (l1**2 - l3**2 + l**2 + (2*x**2) - (2*x*c)) / (2*l)
        z = mp.sqrt(l1**2 - x**2)
        w = mp.sqrt(l3**2 - x**2)
        if (l4 - z - w) <= 0.0001:
            print("la plateforme est en (",x,",", y,") \n")
        else:
           print("erreur: ",x,",",y,"\n")


vmax=20
cmax=10
Mot=[]
for i in range(4):
    m=FakeMotor(100*i,vmax,cmax,i)
    Mot.append(m)
Mot[0].pos=0
Mot[1].pos=50
Mot[2].pos=mp.sqrt(50**2+50**2)
Mot[3].pos=50
Remote=RemoteMotor(Mot, 50, 50, vmax)
Remote.positions()
for i in range(4):
    Mot[i].start()
    
d=1
while(d==1):
    c=int(input("Choix du mode: \n 1- parcours \n 2-pilotage \n 3-arrêter \n"))
    if (c==1):
        print("lancement du parcours \n")
        Remote.parcour()
    elif(c==2):
        x=int(input(("Position en x? \n")))
        y=int(input(("Position en y? \n")))
        
        Remote.movemot(x, y)
    else:
        d=0

del Mot, m, Remote