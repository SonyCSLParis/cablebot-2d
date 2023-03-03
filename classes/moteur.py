# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 17:32:07 2022

@author: angab
"""
import math as mp
import matplotlib.pyplot as plt

#calcul des positions (x,y) de la plateforme mobile
def calcul_pos(lon, lar, focus):
    xsize=int(lon//focus)
    ysize=int(lar//focus)
    size=xsize*ysize
    Pos=[[0,0]]*size
    c=0
    u=1
    carre=focus/2
    for i in range (ysize):
        if (u>=0):
            for j in range (xsize):
                Pos[c]=[carre+i*focus, u*carre+j*focus]
                c=c+1
            u=-u
        
        elif (u<=0):
            for j in range (xsize):
                Pos[c]=[carre+i*focus, u*carre+(xsize-j)*focus]
                c=c+1
            u=-u
        
    X=[]
    Y=[]
    for i in range (len(Pos)):
        X.append(Pos[i][0])
        Y.append(Pos[i][1])
    
    print("Voici les positions de la matrice de votre champs")
    plt.figure(1)
    plt.plot(X,Y,c="blue",ls="-",marker="+")
    plt.show(block=False)
    return Pos


#calcul des positions que le moteur devra avoir en tour
def calcul_pos_mot(L, lon, lar, Tour): #à adapter au test en cours en fonction du nombre de moteur utilisés
    Mot=[[0,0]]*len(L)
    k1=Tour[0]
    k2=Tour[1]
    #k3=Tour[2]
    #k4=Tour[3]
    for i in range (len(L)):
        y=L[0]
        x=L[1]
        d=0.5
        Conv=0.25 #à definir avant
        #print(x,y)
        l1=mp.sqrt(x**2+y**2)
        l1=mp.sqrt(l1**2+d**2)
        #plt.plot(i,l1,color='red',marker='x')
        l2=mp.sqrt((lon-x)**2+y**2)
        l2=mp.sqrt(l2**2+d**2)
        #plt.plot(i,l2,color='green',marker='x')
        #l3=mp.sqrt(x**2+(lar-y)**2)
        #l3=mp.sqrt(l3**2+d**2)
        #plt.plot(i,l3,color='blue',marker='x')
        #l4=mp.sqrt((lon-x)**2+(lar-y)**2)
        #l4=mp.sqrt(l4**2+d**2)
        #plt.plot(i,l4,color='yellow',marker='x')
        #0,5 à changer car juste le rapport de m.tour-1
        c1=round((l1/Conv)-k1)
        c2=round((l2/Conv)-k2)
        #c3=round((l3/0.5)-k3)
        #c4=round((l4/0.5)-k4)
        #k3=l3/Conv
        #k4=l4/Conv
        Mot=[c1,c2]
    return Mot

#interpolatoin via les vitesses de chaque moteur et une constante de temps
def interpol(L):
    vel_max=0.5
    Vel=[[0, 0]]*len(L)
    maxi=L[0]
    V1=0
    V2=0
    #V3=0
    #V4=0
    C=L[1]
    if abs(C)>=maxi:
        maxi=abs(C)
    T=maxi/vel_max #temps en seconde
    V1=L[0]/T
    V2=L[1]/T
    #V3=C[2]/T
    #V4=C[3]/T
    Vel=[V1, V2,int(T)]
    return Vel

if __name__ == "__main__":
    lon=int(input("quelle est la taille de vôtre champ? \n"))
    lar=int(input("quelle est la largeur de votre champ?\n"))
    focus=float(input("quel est votre focus? \n"))
    Pos=calcul_pos(lon, lar, focus)
"""
X=[]
Y=[]
for i in Pos:
    x=i[0]
    y=i[1]
    X.append(x)
    Y.append(y)
plt.figure(1)
plt.plot(X,Y,color='blue', marker='o', linestyle='',linewidth=0, markersize=12)
plt.figlegend("Matrice position")
plt.xlabel('position x')
plt.ylabel('position y')

Mot=calcul_pos_mot(Pos, lon, lar)
Vel=interpol(Mot)
Y1=[]
Y2=[]
Y3=[]
Y4=[]
X=[]
for i in range(0, len(Vel)):
    for j in range (0, Vel[i][4]):
        Y1.append(Vel[i][0])
        Y2.append(Vel[i][1])
        Y3.append(Vel[i][2])
        Y4.append(Vel[i][3])
        X.append(i)
    
plt.figure(1)
plt.figlegend("Moteur 1")
plt.plot(X,Y1)

plt.figure(2)
plt.figlegend("Moteur 2")
plt.plot(X,Y2)

plt.figure(3)
plt.figlegend("Moteur 3")
plt.plot(X,Y3)

plt.figure(4)
plt.figlegend("Moteur 4")
plt.plot(X,Y4)
"""