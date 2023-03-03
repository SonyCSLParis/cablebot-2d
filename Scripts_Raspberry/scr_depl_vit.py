import odrive
import odrive.enums as od
import time

odrv0 = None

try:
    # Recherche d'un ODrive connecté
    odrv0 = odrive.find_any()
    odrv0.axis0.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
    #Mode controle en vitesse
        
    odrv0.axis0.controller.config.control_mode = od.CONTROL_MODE_VELOCITY_CONTROL
    print("Avance: vitesse 1")
    odrv0.axis0.controller.input_vel = 7
    print("Stop")
    time.sleep(2)
    odrv0.axis0.controller.input_vel = 0
    print("Recule: vitesse 1")
    time.sleep(0.2)
    odrv0.axis0.controller.input_vel = -7
    print("Stop")
    time.sleep(2)
    odrv0.axis0.controller.input_vel = 0
    time.sleep(0.2)
    print("Fin.")
    print("Avance: vitesse 1")
    odrv0.axis0.controller.input_vel = 7
    print("Stop")
    time.sleep(2)
    odrv0.axis0.controller.input_vel = 0
    print("Recule: vitesse 1")
    time.sleep(0.2)
    odrv0.axis0.controller.input_vel = -7
    print("Stop")
    time.sleep(5)
    odrv0.axis0.controller.input_vel = 0
    print("Fin.")
    
except BaseException as e:  
    print("Impossible de se connecter à l'ODrive : {}".format(e)) 
