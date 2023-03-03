import odrive
import odrive.enums as od
import time

odrv0 = None

try:
    # Recherche d'un ODrive connecté
    odrv0 = odrive.find_any()
    
    #Mode controle en position
    
    odrv0.axis0.requested_state = od.AXIS_STATE_CLOSED_LOOP_CONTROL
    
    odrv0.axis0.controller.config.control_mode = 3 #(fix me, controle position)
    
    
    print( odrv0.axis0.controller.input_pos )
    print("1 tour en arrière.")
    odrv0.axis0.controller.input_pos = 0.3
    
    time.sleep(5)
    
    print("1 tour en avant.")
    odrv0.axis0.controller.input_pos = 0.8
    

    time.sleep(5)
    print("Fin.")

except BaseException as e:  
    print("Impossible de se connecter à l'ODrive : {}".format(e)) 
