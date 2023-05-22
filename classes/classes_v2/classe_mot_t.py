# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:32:28 2023

@author: angab
"""

import time 
#import matplotlib.pyplot as plt
import odrive
import odrive.enums as od

def pause(t):
    time.sleep(t)
    return


class FakeMotorT:
    def __init__(self, vmax, cmax,tmax):
        self.vmax = vmax #vitesse max
        self.mode=None
        self.tmax=tmax
    
    def get(self):
        print("connection Moteur")
        return 0
    
    def end(self):
        print("Deconnexion moteur")
        return 
    
    def run_m(self, mess):
        mode=mess[2]
        print("message recu: ",mess,"\n")
        """
        Cas END
        """
        if (mode=="E"):
            return False
        
        """
        Cas Switch
        """
        if (mode=="S"):
            switch=mess[4]
            self.switch_mode(switch)
            return True
        
        
        """
        Cas Go
        """
        if (mode=="G"):
            i=4
            test=mess[i]
            val=[]
            while (test!=" "):
                #print(test)
                i=i+1
                val.append(test)
                test=mess[i]
            val=float("".join(val))
            print("val: ",val)
            i=i+1
            test=mess[i]
            T=[]
            while (test!="'"):
                #print(test)
                i=i+1
                T.append(test)
                test=mess[i]
            T=float("".join(T))
            print("T :",T)
            self.go(val,T)
            return True
    
    
    def switch_mode(self, m):
        if m=='v':
            print("passage en mode vitesse \n")
            self.mode="v"
        elif m=='t':
            print("passage en mode torque \n")
            self.mode='t'
        
        else:
            print("erreur ceci n'est pas un mode \n")
        return
    
    def go(self, val, T):
        if self.mode=='v':
            print("vroum vroum, le moteur tourne à la vitesse : ",val,"\n")
            pause(T)
            self.state=True
            print("Stop \n")
        else:
            print("le moteur applique le couple: 0.1 \n")
            pause(T)
        return
    
    """
    def resume(self):
        print(self.X)
        plt.figure(1)
        plt.title("graph resume des consignes de vitesse "+self.name)
        plt.plot(self.X,self.V,c="blue",ls="-",marker="+")
        pause(0.5)
        plt.figure(2)
        plt.title("graph resume des consignes de couple "+self.name)
        plt.plot(self.X,self.T,c="red",ls="-",marker="+")
        plt.xlabel("position")
        plt.ylabel("Valeur")
        plt.show(block=False)
    """


class OdriveMot:
    def __init__(self, vmax, cmax, tmax):
        self.odrv=None
        self.vmax=vmax
        self.cmax=cmax
        self.mode='v'
        self.tmax=tmax
        #self.state=True
    
    def get(self):
        try:
            # Recherche d'un ODrive connecté
            #self.state=False
            self.odrv = odrive.find_any()
            time.sleep(5)
            #print(self.odrv)
            if self.odrv==None:
                print("EROR Motor Not Found!")
                return -1
            ax=self.odrv.axis0
            # Configuration de l'encodeur
            print("2. Configuration de l'encodeur")
            ax.encoder.config.cpr = 8192 # Resolution de l'encodeur (impulsions/tour)
            ax.encoder.config.mode = od.ENCODER_MODE_INCREMENTAL
        
            # Configuration du moteur
            print("3. Configuration du moteur")
            ax.motor.config.current_lim = 15.0 # Limite de courant (A)
            ax.motor.config.calibration_current = 5.0 # Courant de calibration (A)
            ax.motor.config.pole_pairs = 7 # Nombre de paires de poles
            ax.motor.config.motor_type = od.MOTOR_TYPE_HIGH_CURRENT # Type de moteur
            ax.controller.config.vel_limit = 100 # Limite de vitesse (tr/min)

            # Calibration du moteur et de l'encodeur
            print("4. AXIS_STATE_FULL_CALIBRATION_SEQUENCE")
            ax.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE

            # Attendre que la sequence de calibration soit terminee
            print("5. while not AXIS_STATE_IDLE")
            while ax.current_state != od.AXIS_STATE_IDLE:
                time.sleep(0.1)

            # Définir l'état actuel de l'axe
            print("6. AXIS_STATE_CLOSED_LOOP_CONTROL")
            ax.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
            
            #initialisation mode de contrôle
            print("passage en mode velocity")
            ax.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
            
            print("Initialisation du moteur terminée.")
            #self.state=True
            return 0

        except BaseException as e:
            print("Une erreur est survenue:", e)
            return -1
     
    def switch_mode(self,mod):
        if mod==self.mode:
            print("mode inchangé")
            return 0
        elif mod=="v":  
            self.odrv.axis0.controller.input_torque = 0.0
            self.odrv.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
            self.mode=mod
            print("mode passé en vitesse")
            return 0
        elif mod=="t":    
            self.odrv.axis0.controller.config.control_mode = 1
            self.mode=mod
            print("mode passé en couple")
            self.odrv.axis0.controller.input_torque = 0.1
            return 0
        else:
            print("Ceci n'est pas un mode valide")
            return -1
        
    
    def go(self,val,T):
        if T<0:
            print("Erreur temps invalide")
            return -1
        if T==0:
            self.odrv.axis0.controller.input_vel = float(0)
            print("On reste à l'arrêt")
        elif self.mode=="v":
            if abs(val)>abs(self.vmax):
                print("Consigne trop rapide")
                return -1
            #self.state=False
            print("vroum vroum ça tourne")
            self.odrv.axis0.controller.input_vel = float(val)
            time.sleep(T)
            self.odrv.axis0.controller.input_vel = float(0)
            #self.state=True
            return 0
        elif self.mode=="t":
            pass
            #self.state=True
            return 0
        
    def end(self):
        self.odrv.axis0.requested_state=od.AXIS_STATE_IDLE
        self.odrv=None
    
    def run_m(self,mess):
        mode=mess[2]
        print(mess)
        print("mode: ",mode)
        """
        Cas END
        """
        if (mode=="E"):
            self.end()
            return False
        
        """
        Cas Switch
        """
        if (mode=="S"):
            switch=mess[4]
            test=self.switch_mode(switch)
            if test==-1:
                return False
            return True
        
        
        """
        Cas Go
        """
        if (mode=="G"):
            print("go mode activate")
            i=4
            test=mess[i]
            val=[]
            while (test!=" "):
                #print(test)
                i=i+1
                val.append(test)
                test=mess[i]
            val=float("".join(val))
            print("val: ",val)
            i=i+1
            test=mess[i]
            T=[]
            while (test!="'"):
                #print(test)
                i=i+1
                T.append(test)
                test=mess[i]
            T=float("".join(T))
            print("T :",T)
            test=self.go(val,T)
            if test==-1:
                return False
            return True
       
        