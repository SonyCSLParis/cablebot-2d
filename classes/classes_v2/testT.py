# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math as mp
import matplotlib.pyplot as plt
import classe_mot_t as mot



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

def calcul_pos_mot(L, lon, lar, Tour): #à adapter au test en cours en fonction du nombre de moteur utilisés
    C1=Tour[0]
    C2=Tour[1]
    C3=Tour[2]
    C4=Tour[3]
    #print("C1", C1)
    #print("C2", C2)
    #k3=Tour[2]
    #k4=Tour[3]
    y=L[0]
    x=L[1]
    d=0.5
    Conv=0.25 #à definir avant
    #print(x,y)
    l1=mp.sqrt(x**2+y**2)
    #print("l1: ",l1)
    l1=mp.sqrt(l1**2+d**2)
    angle1=mp.atan(d/l1)
    #print("angle1 : ", angle1)
    tor1=calc_torque(angle1, l1)
    #plt.plot(1,l1,color='red',marker='x')
    
    l2=mp.sqrt((lon-x)**2+y**2)
    #print("l2", l2)
    l2=mp.sqrt(l2**2+d**2)
    angle2=mp.atan(d/l2)
    #print("angle2 : ", angle2)
    tor2=calc_torque(angle2, l2)
    #plt.plot(1,l2,color='green',marker='x')
   
    l3=mp.sqrt(x**2+(lar-y)**2)
    l3=mp.sqrt(l3**2+d**2)
    angle3=mp.atan(d/l3)
    tor3=calc_torque(angle3, l3)
    #plt.plot(1,l3,color='blue',marker='x')
    
    l4=mp.sqrt((lon-x)**2+(lar-y)**2)
    l4=mp.sqrt(l4**2+d**2)
    angle4=mp.atan(d/l4)
    tor4=calc_torque(angle4, l4)
    #plt.plot(1,l4,color='yellow',marker='x')
    #0,5 à changer car juste le rapport de m.tour-1
    t1=(l1/Conv)
    t2=(l2/Conv)
    t3=(l3/Conv)
    t4=(l4/Conv)
    c1=t1-C1
    c2=t2-C2
    c3=t3-C3
    c4=t4-C4
    
    Cons=[c1,c2,c3,c4]
    Tour=[t1,t2,t3,t4]
    Tor=[tor1,tor2,tor3,tor4]
    return Cons, Tour, Tor


def calc_t(C):
    vmax=8; #vitesse max en tour.sec-1
    T=C/vmax;
    return T

def calc_vit(T,C):
    return C/T

def calc_torque(angle, l):
    P=1/4;
    return 50*P*mp.sin(angle)*l


if __name__=="__main__":
    Pos = calcul_pos(5,5,1)
    Tour=[0,25,25,35]
    mot1=mot.FakeMotorT(2,2,0,'mot 1')
    mot2=mot.FakeMotorT(2,2,25,'mot 2')
    mot3=mot.FakeMotorT(2,2,25,'mot 3')
    mot4=mot.FakeMotorT(2,2,35,'mot 4')
    Mot=[mot1,mot2,mot3,mot4]
    for i in range(len(Pos)):
        Cons, Tour, Tor =calcul_pos_mot(Pos[i],5,5, Tour)
        #print("Cons=",Cons)
        for j in range(4):
            if (Cons[j]<0):
                Mot[j].switch_mode('t')
            else:
                Mot[j].switch_mode('v')
        T=0.5
        for j in range(4):
            #print(Mot[j].mode)
            if Mot[j].mode=="v":
                temp=calc_t(Cons[j])
                #print("temp=",temp)
                if temp>=T:
                    T=temp
        #print("T= ",T)
        for j in range(4):
            if Mot[j].mode=="v":
                val=calc_vit(T,Cons[j])
                Mot[j].go(val,T)
            else:
                Mot[j].go(Tor[j],T)
    
    print("resume des consgines du moteur")
    for i in range(4):
        Mot[i].resume()

