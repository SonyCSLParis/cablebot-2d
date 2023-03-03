# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:38:38 2023

@author: angab
"""
import odrive
import odrive.enums as od
import time 

def pause(t):
    time.sleep(t)
    return

class Motor:
    def __init__(self, vmax, cmax):
        self.vmax = vmax #vitesse max
        self.pos=0#nombre de tour que le moteur a efféctué
            


class OdriveMotor(Motor):
    def __init__(self,vmax,cmax,serial):
        super().__init__(vmax,cmax)
        self.serial=serial
        self.odrv = None
    
    def get(self):
        try:
            # Recherche d'un ODrive connecté
            odrv0 = odrive.find_any(serial_number=self.serial)

            # Configuration du moteur
            # Définir le mode de contrôle
            odrv0.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
            odrv0.axis0.motor.config.current_lim = 10.0 # Limite de courant (A)
            odrv0.axis0.motor.config.calibration_current = 5.0 # Courant de calibration (A)
            odrv0.axis0.motor.config.pole_pairs = 7 # Nombre de paires de pôles
            odrv0.axis0.motor.config.motor_type = od.MOTOR_TYPE_HIGH_CURRENT # Type de moteur
            odrv0.axis0.encoder.config.mode = od.ENCODER_MODE_HALL # Mode d'encodeur
            odrv0.axis0.controller.config.vel_limit = 2000.0 # Limite de vitesse (tr/min)

            # Configuration de l'encodeur
            odrv0.axis0.encoder.config.cpr = 42 # Résolution de l'encodeur (impulsions/tour)

            # Calibration du moteur et de l'encodeur
            odrv0.axis0.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE

            # Attendre que la séquence de calibration soit terminée
            while odrv0.axis0.current_state != od.AXIS_STATE_IDLE:
                time.sleep(0.1)

            # Définir l'état actuel de l'axe
            odrv0.axis0.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
            
            
            print("Initialisation du moteur terminée.")

        except Exception as e:
            print("Une erreur est survenue:", e)
    
    def moveto(self,vit,T):
        self.odrv.axis0.controller.vel_setpoint = vit * self.odrv.axis0.encoder.config.cpr / 60.0
        pause(T)
        self.odrv.axis0.controller.input_vel = 0
        
        
class FakeMotor(Motor):
    def __init__(self, vmax, cmax):
       super().__init__(vmax,cmax)
    
    def get(self):
        print("connected")
    
    def moveto(self,vit,T):
        print("vroum vroum à la vitesse: ",vit)
        pause(T)
        print("stop on s'arrête!")
        
        
        
        
"""
class RemoteMotor:
    def __init__(self,Motor,host,port):
        self.Motor=Motor
        self.host=host
        self.port=port
        
"""  