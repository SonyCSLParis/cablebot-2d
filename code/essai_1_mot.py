# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 16:50:36 2023

@author: angab
"""
import odrive
import odrive.enums as od
import time

def pause(t):
    """
    fonction pour attendre la réalisation physique
    """
    print("Pause started")
    time.sleep(t)
    print("Pause ended")


odrv = odrive.find_any()
axis = odrv.axis0


odrv.config.enable_brake_resistor = True
odrv.config.brake_resistance = 2                                     # resistance connecté au AUX sur la carte
axis.controller.config.vel_limit = 20                                       # rps limit
axis.motor.config.pole_pairs = 7                                            # Datasheet extracted value
axis.motor.config.torque_constant = 8.27/270                                # Motor K_v = 270 rpm/V
axis.motor.config.motor_type = 0                                            # MOTOR_TYPE_HIGH_CURRENT since we're using a BLDC.
axis.encoder.config.cpr = 8192                                             # Counts per revolution. cf. AMT102-V datahsheet, DIP Switch
pause(2)
print("etape 1: calibration")
axis.requested_state = od.AXIS_STATE_FULL_CALIBRATION_SEQUENCE                 # Motor calibration state
pause(20)
print(axis.active_errors)
axis.encoder.config.use_index = True   
print("etape 2: index")                                     # We're using the encoder's Z output to calibrate the latter through stored index
axis.requested_state = od.AXIS_STATE_ENCODER_INDEX_SEARCH                      # The motor will turn until it finds the index
pause(20)
print(axis.active_errors)
print("etape 3: offset")
axis.requested_state = od.AXIS_STATE_ENCODER_OFFSET_CALIBRATION                # Then it will calibrate
pause(20)
print(axis.active_errors)
"""
axis.encoder.config.pre_calibrated = True                                   # Boolean values indicating everything is calibrated for future uses
axis.config.startup_encoder_index_search = True
axis.motor.config.pre_calibrated = True
"""

axis.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
axis.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
while True:
    try:
        speed = float(input("Entrer la vitesse en tour/s (0 pour quitter): "))
        if speed == 0:
            break
        axis.controller.input_vel = speed
    except ValueError:
        print("Entrée non valide, veuillez entrer un nombre.")

axis.controller.input_vel = 0                                             #
axis.controller.input_pos = axis.encoder.pos_estimate                       # ensures that on power on, the motors won't go to a faraway position
axis.requested_state = od.AXIS_STATE_IDLE