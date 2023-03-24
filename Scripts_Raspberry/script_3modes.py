# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:54:45 2023

@author: angab
"""

import odrive
import odrive.enums as od
#from fibre.protocol import ChannelBrokenException
import time

odrv0 = None

try:
    # Recherche d'un ODrive connecté
    print("1. odrive.find_any.")
    odrv0 = odrive.find_any()

    conf = input("faut-il reconfigurer, o pour oui    ")

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

        mode = (input("Quel mode: v pour vitesse, p position, c couple, t pour trajectoire    "))
        if mode == "v":
            while True:
                odrv0.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
                vit = input("Quel vitesse? Tapper s pour changer de mode")
                if vit == "s":
                    break
                else :
                    odrv0.axis0.controller.input_vel = float(vit)
            
        if mode == "p":
            while True:
                odrv0.axis0.controller.config.control_mode = 3 # mode position
                pos = input("Quel position? Tapper s pour changer de mode")
                if pos == "s":
                    break
                else :
                    odrv0.axis0.controller.input_pos = float(pos)
                    time.sleep(1)

    
        
        if mode == "c":
            while True:
                odrv0.axis0.controller.config.control_mode = 1 #torque control
                # Approximately 8.23 / Kv where Kv is in the units [rpm / V]
                odrv0.axis0.motor.config.torque_constant = 8.23 / 150
                couple = input("Quel couple? Tapper s pour changer de mode")
                if couple == "s":
                    break
                else :
                    odrv0.axis0.controller.input_torque = float(couple)
                
        if mode == "t":
            while True:
                odrv0.axis0.controller.config.control_mode = 3 # mode position
                odrv0.axis0.controller.config.input_mode = od.InputMode.TRAP_TRAJ
                vit = input("Entrer la vitesse max à atteindre (valeur POSITIVE)? Tapper s pour changer de mode")
                acc = input("Entrer l'accel max (valeur POSITIVE)? Tapper s pour changer de mode")
                decel = input("Entrer la decel max (valeur POSITIVE)? Tapper s pour changer de mode")
                odrv0.axis0.trap_traj.config.accel_limit = float(acc)
                odrv0.axis0.trap_traj.config.accel_limit = float(decel)
                odrv0.axis0.trap_traj.config.vel_limit = float(vit)
                if decel or acc or vit == "s":
                    break
                else :
                    odrv0.axis0.controller.input_torque = float(couple)
            
            
        

    
except BaseException as e:  
    print("Impossible de se connecter à l'ODrive : {}".format(e))