# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:32:28 2023

@author: angab
"""

import time 
import matplotlib.pyplot as plt
import odrive
import odrive.enums as od

def pause(t):
    time.sleep(t)
    return


class FakeMotorT:
    def __init__(self, vmax, cmax, pos,name):
        self.vmax = vmax #vitesse max
        self.pos=pos#nombre de tour que le moteur a efféctué
        self.mode=None
        self.name=name
        self.X=[0]
        self.V=[0]
        self.T=[0]
        self.state=True
    
    def run_m(self, mess):
        mode=mess[2]
        print(mess)
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
        
        """
        Cas Resume
        """
        if (mode=="R"):
            self.resume()
    
    def switch_mode(self, m):
        if m=='v':
            #print("passage en mode vitesse")
            self.mode="v"
        elif m=='t':
            #print("passage en mode torque")
            self.mode='t'
        
        else:
            print("erreur ceci n'est pas un mode")
        return
    
    def go(self, val, T):
        t=self.X[-1]
        if self.mode=='v':
            self.state=False
            self.V.append(val)
            self.T.append(0)
            self.X.append(t+1)
            #print("vroum vroum, le moteur tourne à la vitesse : ",val)
            pause(T)
            self.state=True
            #print("Stop")
        else:
            self.state=False
            self.T.append(val)
            self.V.append(0)
            self.X.append(t+1)
            #print("le moteur applique le couple: ",val)
            pause(T)
            self.state=True
            #print("Stop")
        return
    
    def resume(self):
        plt.figure(1)
        plt.title("graph resume des consignes du moteur "+self.name)
        plt.plot(self.X,self.V,c="blue",ls="-",marker="+")
        pause(0.5)
        plt.plot(self.X,self.T,c="red",ls="-",marker="+")
        plt.xlabel("position")
        plt.ylabel("Valeur")
        plt.legend("Vitesse","Torque")
        plt.show(block=False)



class OdriveMot:
    def __init__(self, vmax, cmax, tmax):
        self.odrv=None
        self.vmax=vmax
        self.cmax=cmax
        self.mode=None
        self.tmax=tmax
    
    def get(self):
        try:
            # Recherche d'un ODrive connecté
            self.odrv = odrive.find_any()
            ax=self.odrv.axis0
            # Configuration du moteur
            # Définir le mode de contrôle
            ax.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
            ax.motor.config.current_lim = self.cmax # Limite de courant (A)
            ax.motor.config.calibration_current = 5.0 # Courant de calibration (A)
            ax.motor.config.pole_pairs = 7 # Nombre de paires de pôles
            ax.motor.config.motor_type = od.MOTOR_TYPE_HIGH_CURRENT # Type de moteur
            ax.encoder.config.mode = od.ENCODER_MODE_HALL # Mode d'encodeur
            ax.controller.config.vel_limit = self.vmax # Limite de vitesse (tr/min)
            ax.motor.config.torque_constant = 8.23 / 150

            # Configuration de l'encodeur
            ax.encoder.config.cpr = 42 # Résolution de l'encodeur (impulsions/tour)

            # Calibration du moteur et de l'encodeur
            ax.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE

            # Attendre que la séquence de calibration soit terminée
            while ax.current_state != od.AXIS_STATE_IDLE:
                time.sleep(0.1)

            # Définir l'état actuel de l'axe
            ax.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
            
            
            print("Initialisation du moteur terminée.")
            return 0

        except Exception as e:
            print("Une erreur est survenue:", e)
            return -1
     
    def switch_mode(self,mod):
        if mod=="V":    
            self.odrv.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
            self.mode=mod
            return 0
        elif mod=="T":    
            self.odrv.axis0.controller.config.control_mode = 1
            self.mode=mod
            return 0
        else:
            print("Ceci n'est pas un mode valide")
            return -1
        
    
    def go(self,val,T):
        if T<=0:
            print("Erreur temps invalide")
            return -1
        elif self.mode=="V":
            if val>self.vmax:
                print("Consigne trop rapide")
                return -1
            self.odrv.axis0.controller.input_vel = val
            time.sleep(T)
            self.odrv.axis0.controller.input_vel = 0
            return 0
        elif self.mode=="T":
            if val>self.tmax:
                print("Couple invalide!")
                return -1
            self.odrv.axis0.controller.input_torque = val
            time.sleep(T)
            self.odrv.axis0.controller.input_torque = 0
            return 0
        
    def end(self):
        self.odrv.axis0.requested_state=od.AXIS_STATE_IDLE
        self.odrv=None
    
    def run_m(self,mess):
        mode=mess[2]
        print(mess)
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
            return 0
        
        
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
            test=self.go(val,T)
            if test==-1:
                return False
            return 0
       
        