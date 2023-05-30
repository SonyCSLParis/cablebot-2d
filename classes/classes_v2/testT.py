# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math as mp
#import matplotlib.pyplot as plt



def calcul_pos(lon, lar, focus):
    #print('début calcul pos')
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
       
    #X=[]
    #Y=[]
    #for i in range (len(Pos)):
    #    X.append(Pos[i][0])
    #    Y.append(Pos[i][1])
    
    #print("Voici les positions de la matrice de votre champs")
    #plt.figure(1)
    #plt.plot(X,Y,c="blue",ls="-",marker="+")
    #plt.show(block=False)
    
    return Pos
def calcul_long_mot(L,lon, lar):
    y=L[0]
    x=L[1]
    l1=mp.sqrt(x**2+y**2)
    #print("l1: ",l1)
    #l1=mp.sqrt(l1**2+d**2)
    #print("angle1 : ", angle1)
    #plt.plot(1,l1,color='red',marker='x')
    
    l2=mp.sqrt((lon-x)**2+y**2)
    #print("l2", l2)
    #l2=mp.sqrt(l2**2+d**2)
    #print("angle2 : ", angle2)
    #plt.plot(1,l2,color='green',marker='x')
   
    l3=mp.sqrt(x**2+(lar-y)**2)
    #l3=mp.sqrt(l3**2+d**2)
    #plt.plot(1,l3,color='blue',marker='x')
    
    l4=mp.sqrt((lon-x)**2+(lar-y)**2)
    
    return [l1,l2,l3,l4]

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
    #d=0.5 #battement
    Conv=0.3 #à definir avant
    #print(x,y)
    l1=mp.sqrt(x**2+y**2)
    #print("l1: ",l1)
    #l1=mp.sqrt(l1**2+d**2)
    #print("angle1 : ", angle1)
    #plt.plot(1,l1,color='red',marker='x')
    
    l2=mp.sqrt((lon-x)**2+y**2)
    #print("l2", l2)
    #l2=mp.sqrt(l2**2+d**2)
    #print("angle2 : ", angle2)
    #plt.plot(1,l2,color='green',marker='x')
   
    l3=mp.sqrt(x**2+(lar-y)**2)
    #l3=mp.sqrt(l3**2+d**2)
    #plt.plot(1,l3,color='blue',marker='x')
    
    l4=mp.sqrt((lon-x)**2+(lar-y)**2)
    #l4=mp.sqrt(l4**2+d**2)
    #plt.plot(1,l4,color='yellow',marker='x')
    #0,5 à changer car juste le rapport de m.tour-1
    #print('calcul des tours')
    t1=float((l1/Conv))
    t2=float((l2/Conv))
    t3=float((l3/Conv))
    t4=float((l4/Conv))
    #print('calcul des consignes')
    #print('C1: ',C1)
    #print('C2: ',C2)
    #print('C3: ',C3)
    #print('C4: ',C4)
    c1=t1-C1
    c2=t2-C2
    c3=t3-C3
    c4=t4-C4
    
    Cons=[c1,c2,c3,c4]
    Tour=[t1,t2,t3,t4]
    return Cons, Tour

def pos_plan():
    Cons=[[0,0],[1,1],[1,0],[2,2],[0,0],[0,2],[1,1],[0,0]]
    return Cons

def calcul_pos_mot_plan(Cons):
    
    L=[]
    for i in Cons:
        x=i[0]
        y=i[1]
        l1=mp.sqrt(x**2+y**2)
        l2=mp.sqrt((3-x)**2+y**2)
        l3=mp.sqrt((3-x)**2+(3-y)**2)
        l4=mp.sqrt(x**2+(3-y)**2)
        l=[l1,l2,l3,l4]
        L.append(l)
    print("L= ",L)
    return L

def calc_tour_ligne(L,T,conv):
    t1=T[0]
    t2=T[1]
    t3=T[2]
    t4=T[3]
    Mot=[]
    for i in L:
        m1=(i[0]/conv)-t1
        m2=(i[1]/conv)-t2
        m3=(i[2]/conv)-t3
        m4=(i[3]/conv)-t4
        t1=m1+t1
        t2=m2+t2
        t3=m3+t3
        t4=m4+t4
        m=[m1,m2,m3,m4]
        Mot.append(m)
    #print("Mot: ",Mot)
    return Mot

def calc_t(C):
    vmax=3; #vitesse max en tour.sec-1
    T=C/vmax;
    return abs(T)

def calc_vit(T,C):
    if T==0:
        return 2
    if C==0:
        return 2
    return C/T

"""
if __name__=="__main__":
"""
"""
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
    """
"""   
    Pos = pos_ligne()
    T=[12,12]
    L=calcul_pos_mot_ligne(Pos)
    Mot=calc_tour_ligne(L, T)
    X=[]
    Py=[]
    L1=[]
    L2=[]
    M1=[]
    M2=[]
    for i in range(len(Pos)):
        X.append(i)
        
        #Pos
        Py.append(Pos[i][0])
        
        #L
        L1.append(L[i][0])
        L2.append(L[i][1])
        
        #Mot
        M1.append(Mot[i][0])
        M2.append(Mot[i][1])
    
    plt.figure(1)
    plt.title("Positions de la ligne")
    plt.plot(X,Py,c="blue",ls="-",marker="+")
    plt.show(block=False)
    
    plt.figure(2)
    plt.title("Longueur des câbles")
    plt.plot(X,L1,c="red",marker="+")
    plt.plot(X,L2,c="blue",marker="+")
    plt.show(block=False)
    
    plt.figure(3)
    plt.title("Consignes tours moteur 1")
    plt.plot(X,M1,c="green",marker="+")
    plt.show(block=False)
    
    plt.figure(4)
    plt.title("Consigne tours moteur 2")
    plt.plot(X,M2,c="purple",marker="+")
    plt.show(block=False)

    #print(L1)
    #print(L2)
"""   
