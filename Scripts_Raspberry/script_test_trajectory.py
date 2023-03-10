# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:44:29 2023

@author: angab
"""

import odrive as o
import odrive.enums as od
import time

odrv0 = None

init=int(input("Voulez vous initialiser le moteur? \n 1- Oui \n 2- Non"))
if init==1:
    try:
        # Recherche d'un ODrive connecté
        print("1. odrive.find_any.")
        odrv0 = o.find_any()

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
    
    except BaseException as e:  
       print("Impossible de se connecter à l'ODrive : {}".format(e))

try:
    print("Début de contrôle en trajectoire")

    odrv0.axis0.trap_traj.config.vel_limit = 20
    odrv0.axis0.trap_traj.config.accel_limit = 10
    odrv0.axis0.trap_traj.config.decel_limit = 10
    odrv0.axis0.config.motor.current_soft_max = 10

    odrv0.axis0.controller.config.input_mode = od.InputMode.TRAP_TRAJ

    print("Test pour 100 tours")
    odrv0.axis0.controller.move_incremental(100, from_goal_point=True)
    while odrv0.axis0.current_state != od.AXIS_STATE_CLOSED_LOOP_CONTROL:
        pass
    while odrv0.axis0.current_state != od.AXIS_STATE_IDLE:
        pass
    print("Test pour -100 tours")
    odrv0.axis0.controller.move_incremental(-100, from_goal_point=True)
    while odrv0.axis0.current_state != od.AXIS_STATE_CLOSED_LOOP_CONTROL:
        pass
    while odrv0.axis0.current_state != od.AXIS_STATE_IDLE:
        pass
    print("Fin test")
    odrv0.axis0.requested_state = od.AXIS_STATE_IDLE
except BaseException as e:  
    print("Echec dans le contrôle en trajectoire : {}".format(e))