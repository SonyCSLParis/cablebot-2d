import math
import argparse
from spidercam import * 

class RealSpidercamFactory():
    
    def __init__(self, field_width, field_height):
        real_diameter = 0.03 # 3 cm
        distance_per_revolution = math.pi * real_diameter
        serial_id_0 = "xyz" # TODO: read from config file? OK to hardcode for now.
        serial_id_1 = "abc"
        self.field_width = field_width
        self.field_height = field_height
        self.motorcontroller_0 = OdriveBoard(serial_id_0, distance_per_revolution)
        self.motorcontroller_1 = OdriveBoard(serial_id_1, distance_per_revolution)
    
    def get_motors(self):
        motors = [None, None, None, None]
        motors[0] = self.motorcontroller_0.get_motor(0)
        motors[1] = self.motorcontroller_0.get_motor(1)
        motors[2] = self.motorcontroller_1.get_motor(0)
        motors[3] = self.motorcontroller_1.get_motor(1)
        return motors
    
    def get_camera(self):
        return FakeCamera(1024, 768)
        
    def get_filesystem(self):
        return Filesystem('.')


class TestSpidercamFactory():
    
    def __init__(self, field_width, field_height):
        self.field_width = field_width
        self.field_height = field_height
    
    def get_motors(self):
        maximum_position = math.sqrt(self.field_width**2 + self.field_height**2)
        maximum_speed = 0.5 # m/s
        motors = [None, None, None, None]
        motors[0] = FakeMotor(0, maximum_position, maximum_speed)
        motors[1] = FakeMotor(0, maximum_position, maximum_speed)
        motors[2] = FakeMotor(0, maximum_position, maximum_speed)
        motors[3] = FakeMotor(0, maximum_position, maximum_speed)
        return motors
        
    def get_camera(self):
        return FakeCamera(1024, 768)
        
    def get_filesystem(self):
        return Filesystem('.')

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--field-width", default=30) 
    parser.add_argument("--field-height", default=30)
    parser.add_argument("-t", "--test", help="Run test code", action="store_true")
    args = parser.parse_args()

    # The factory groups all the specifics. All the remainin code
    # should be generic.
    if args.test:
        factory = TestSpidercamFactory(args.field_width, args.field_height)
    else:
        factory = RealSpidercamFactory(args.field_width, args.field_height)
        
    motors = factory.get_motors()
    camera = factory.get_camera()
    filesystem = factory.get_filesystem()

    # Create the SpiderCam
    device = SpiderCam(field_width, field_height, motors, camera, filesystem)

    device.moveto(field_width/2, field_height/2)
    device.grab()
    
if __name__ == "__main__":
    main()



