# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 16:03:17 2023

@author: angab
"""
import odrive
import odrive.enmus as od
import time

serial=input("numéro de série?")
cmax=input("courant max?")
vmax=input("vitesse max?")


def pause(t = 0.1):
    """
    pas grand-chose à ajouter...
    """
    print("Pause started")
    time.sleep(t)
    print("Pause ended")
    return None

#initialisation des moteurs attention prends du temps (30sec)
odrv=odrive.find_any(serial)#attache du moteur
ax = odrv.axis0
ax.motor.config.pole_pairs = True
odrv.config.dc_bus_overvoltage_trip_level = 40
odrv.config.dc_max_positive_current = cmax#courant max
ax.controller.config.vel_limit = vmax#vitesse max
odrv.config.dc_max_negative_current = -1
odrv.config.brake_resistor0.resistance = 2
odrv.config.brake_resistor0.enable = True
ax.config.motor.motor_type = od.MotorType.HIGH_CURRENT
ax.config.motor.pole_pairs = 7
ax.config.motor.torque_constant = 8.27 / 150
ax.requested_state = od.AxisState.MOTOR_CALIBRATION #calibration des axes qui prends un certains temps
pause(10)
odrv.inc_encoder0.config.cpr = 8192
odrv.inc_encoder0.config.enabled = True
ax.requested_state = od.AxisState.ENCODER_INDEX_SEARCH #création de l'index de notre encodeur
pause(10)
ax.requested_state = od.AxisState.ENCODER_OFFSET_CALIBRATION#calcul de l'offset de l'encodeur
pause(10)
odrv.save_configuration()#sauvegarde de la config pour na pas avoir à la refaire après
