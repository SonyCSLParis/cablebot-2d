import math
import argparse
import spidercam


def main():
    #parser = argparse.ArgumentParser()
    #parser.parse_args()

    # Size of the field
    field_width = 30
    field_length = 30

    # Connect to the motors
    maximum_position = math.sqrt(field_width**2 + field_length**2)
    maximum_speed = 0.5 # m/s
    motorcontroller_0 = spidercam.FakeMotorController(maximum_position, maximum_speed)
    motorcontroller_1 = spidercam.FakeMotorController(maximum_position, maximum_speed)
    motors = [None, None, None, None]
    motors[0] = motorcontroller_0.get_motor(0)
    motors[1] = motorcontroller_0.get_motor(1)
    motors[2] = motorcontroller_1.get_motor(0)
    motors[3] = motorcontroller_1.get_motor(1)

    # Connect to the camera
    camera = spidercam.FakeCamera(1024, 768)

    # Connect to the image storage
    filesystem = spidercam.Filesystem('.')

    # Create the SpiderCam
    device = spidercam.SpiderCam(field_width, field_length, motors, camera, filesystem)

    device.moveto(field_width/2, field_length/2)
    device.grab()
    
if __name__ == "__main__":
    main()



