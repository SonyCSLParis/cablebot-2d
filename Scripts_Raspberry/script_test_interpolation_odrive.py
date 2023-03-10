# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:26:08 2023

@author: angab
"""

import odrive
import odrive.enums as od 
import time

# Se connecter aux quatre ODrive
odrv0 = odrive.find_any(serial_number="serie 1")
odrv1 = odrive.find_any(serial_number="serie 2")
odrv2 = odrive.find_any(serial_number="serie 3")
odrv3 = odrive.find_any(serial_number="serie 4")

# Configurer chaque moteur
axis0 = odrv0.axis0
axis0.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while axis0.current_state != od.AXIS_STATE_IDLE:
    time.sleep(0.1)
axis0.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL

axis1 = odrv1.axis0
axis1.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while axis1.current_state != od.AXIS_STATE_IDLE:
    time.sleep(0.1)
axis1.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL

axis2 = odrv2.axis0
axis2.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while axis2.current_state != od.AXIS_STATE_IDLE:
    time.sleep(0.1)
axis2.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL

axis3 = odrv3.axis0
axis3.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while axis3.current_state != od.AXIS_STATE_IDLE:
    time.sleep(0.1)
axis3.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL

# Activer la fonctionnalité d'interpolation pour chaque ODrive
odrv0.interpolator.config.enabled = True
odrv1.interpolator.config.enabled = True
odrv2.interpolator.config.enabled = True
odrv3.interpolator.config.enabled = True

# Définir les consignes de position pour chaque axe de moteur
odrv0.interpolator.move_to([10000], [10000], [10000], [10000])
odrv1.interpolator.move_to([20000], [20000], [20000], [20000])
odrv2.interpolator.move_to([30000], [30000], [30000], [30000])
odrv3.interpolator.move_to([40000], [40000], [40000], [40000])

# Attendre que le mouvement soit terminé
while odrv0.interpolator.remaining_segments > 0 or odrv1.interpolator.remaining_segments > 0 or odrv2.interpolator.remaining_segments > 0 or odrv3.interpolator.remaining_segments > 0:
    time.sleep(0.1)

# Désactiver la fonctionnalité d'interpolation pour chaque ODrive
odrv0.interpolator.config.enabled = False
odrv1.interpolator.config.enabled = False
odrv2.interpolator.config.enabled = False
odrv3.interpolator.config.enabled = False
