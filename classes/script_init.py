# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:54:45 2023

@author: angab
"""

import odrive
import odrive.enums as od
import time

odrv0 = None

try:
    # Recherche d'un ODrive connecté
    odrv0 = odrive.find_any()

    # Configuration du moteur
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

    # Boucle principale pour contrôler le moteur
    while True:
        # Lecture de la consigne de vitesse
        consigne_vitesse = float(input("Entrez une consigne de vitesse (tr/min): "))

        # Conversion de la consigne en une commande pour le moteur
        commande_moteur = consigne_vitesse / 60.0 * odrv0.axis0.encoder.config.cpr

        # Envoi de la commande au moteur
        odrv0.axis0.controller.vel_setpoint = commande_moteur

        # Lecture de la vitesse réelle du moteur
        vitesse_reelle = odrv0.axis0.encoder.vel_estimate * odrv0.axis0.motor.config.pole_pairs / odrv0.axis0.encoder.config.cpr * 60.0

        # Affichage de la vitesse réelle du moteur
        print("Vitesse réelle du moteur: {:.2f} tr/min".format(vitesse_reelle))
        
except Exception as e:
    print("Une erreur est survenue:", e)
