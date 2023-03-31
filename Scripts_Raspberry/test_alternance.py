# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:34:34 2023

@author: angab
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')

import odrive
import odrive.enums as od
#from fibre.protocol import ChannelBrokenException
import time
time.sleep(0.5)
odrv0 = None

try:
    # Recherche d'un ODrive connecté
    print("1. odrive.find_any.")
    odrv0 = odrive.find_any()
    time.sleep(1)
    conf = input("faut-il reconfigurer, o pour oui    ")
    #print(odrv0)
    if conf == "o":

        # Configuration de l'encodeur
        print("2. Configuration de l'encodeur")
        odrv0.axis0.encoder.config.cpr = 8192 # Résolution de l'encodeur (impulsions/tour)
        odrv0.axis0.encoder.config.mode = od.ENCODER_MODE_INCREMENTAL
        
        # Configuration du moteur
        print("3. Configuration du moteur")
        odrv0.axis0.motor.config.current_lim = 10.0 # Limite de courant (A)
        odrv0.axis0.motor.config.calibration_current = 5.0 # Courant de calibration (A)
        odrv0.axis0.motor.config.pole_pairs = 7 # Nombre de paires de pôles
        odrv0.axis0.motor.config.motor_type = od.MOTOR_TYPE_HIGH_CURRENT # Type de moteur
        odrv0.axis0.controller.config.vel_limit = 100 # Limite de vitesse (tr/min)

        # Calibration du moteur et de l'encodeur
        print("4. AXIS_STATE_FULL_CALIBRATION_SEQUENCE")
        odrv0.axis0.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE

        # Attendre que la séquence de calibration soit terminée
        print("5. while not AXIS_STATE_IDLE")
        while odrv0.axis0.current_state != od.AXIS_STATE_IDLE:
            time.sleep(0.1)

        # Définir l'état actuel de l'axe
        print("6. AXIS_STATE_CLOSED_LOOP_CONTROL")
        odrv0.axis0.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
        
        #position control
        odrv0.axis0.controller.config.control_mode = 3
        


        print("Initialisation du moteur terminée.")

        print("1 tour en avant.")
        odrv0.axis0.controller.input_pos = 0.5

        time.sleep(5)
        
        print("1 tour en arrière.")
        odrv0.axis0.controller.input_pos = 0

        time.sleep(5)
        print("Fin.")
    
    #odrv0.save_configuration()
    while True:
        TEST=int(input("Quel test réaliser? \n 1= alternance couple/vitesse automatique sans raz \n 2= alterance couple/vitesse avec raz \n 3 quitter"))
        if TEST == 3:
            break
        elif TEST == 1:
            i=0
            while i<20:
                odrv0.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
                odrv0.axis0.controller.input_vel = 6
                time.sleep(2)
                odrv0.axis0.controller.config.control_mode = 1 #torque control
                # Approximately 8.23 / Kv where Kv is in the units [rpm / V]
                odrv0.axis0.motor.config.torque_constant = 8.23 / 150
                odrv0.axis0.controller.input_torque = -0.02
                time.sleep(2)
                i+=1
        elif TEST == 2:
            i=0
            while i<20:
                odrv0.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
                odrv0.axis0.controller.input_vel = 6
                time.sleep(2)
                odrv0.axis0.controller.input_vel = 0
                odrv0.axis0.controller.config.control_mode = 1 #torque control
                # Approximately 8.23 / Kv where Kv is in the units [rpm / V]
                odrv0.axis0.motor.config.torque_constant = 8.23 / 150
                odrv0.axis0.controller.input_torque = -0.02
                time.sleep(2)
                odrv0.axis0.controller.input_torque = 0
                i+=1
        else :
            print("ceci n'est pas un des choix proposés")
except BaseException as e:  
    print("Erreur survenue : {}".format(e))