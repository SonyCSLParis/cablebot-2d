# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 17:32:07 2022

@author: angab
"""
import math as mp

def calcul_pos(lon, lar):
    psize=0.95
    xsize=int(lon//psize)
    ysize=int(lar//psize)
    size=xsize*ysize
    Pos=[[0,0]]*size
    c=0
    for i in range (0,ysize):
        for j in range (0, xsize):
            Pos[c]=[0.475+i*psize, 0.475+j*psize]
            c=c+1
    return Pos


def calcul_pos_mot(L, lon, lar):
    Mot=[[0,0,0,0]]*len(L)
    c1=0
    c2=0
    c3=0
    c4=0
    for i in range (len(L)):
        y=L[i][0]
        x=L[i][1]
        l1=mp.sqrt(x**2+y**2)
        l2=mp.sqrt((lon-x)**2+y**2)
        l3=mp.sqrt(x**2+(lar-y)**2)
        l4=mp.sqrt((lon-x)**2+(lar-y)**2)
        c1=int((l1/0.5)-c1)
        c2=int((l2/0.5)-c2)
        c3=int((l3/0.5)-c3)
        c4=int((l4/0.5)-c4)
        Mot[i]=[c1,c2,c3,c4]
    return Mot

def interpol(L):
    vel_max=0.5
    Vel=[[0, 0, 0, 0]]*len(L)
    for i in range(len(L)):
        C=L[i]
        maxi=C[0]
        for j in C:
            if abs(j)>=maxi:
                maxi=abs(j)
        T=maxi/vel_max #temps en seconde
        V1=C[0]/T
        V2=C[1]/T
        V3=C[2]/T
        V4=C[3]/T
        Vel[i]=[V1, V2, V3, V4]
    return Vel

lon=int(input("quelle est la taille de vôtre champ? \n"))
lar=int(input("quelle est la largeur de votre champ?\n"))
Pos=calcul_pos(lon, lar)

Mot=calcul_pos_mot(Pos, lon, lar)

for i in Mot:
    print(i)

Vel=interpol(Mot)

c=0
for i in Vel:
    print(i)