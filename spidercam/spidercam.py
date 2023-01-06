import math
import os
from abc import ABC, abstractmethod
import numpy as np
import cv2

# Interfaces

class IMotorController(ABC):    
    @abstractmethod
    def count_motors(self):
        pass
    
    @abstractmethod
    def get_motor(self, index):
        pass

class IMotor(ABC):    
    @abstractmethod
    def moveto(self, absolute_position, speed):
        pass

    @abstractmethod
    def move(self, relative_distance, speed):
        pass

    @abstractmethod
    def get_position(self):
        pass
    
class ICamera(ABC):    
    @abstractmethod
    def grab(self):
        pass

class IFilesystem(ABC):    
    @abstractmethod
    def store(self, image):
        pass

# Top level objects 

class Box():    
    def __init__(self, motor):
        self.motor = motor
        
    def moveto(self, x, speed):
        self.motor.moveto(x, speed)


class SpiderCam():    
    def __init__(self, width, length, motors, camera, filesystem):
        self.width = width
        self.length = length
        self.motors = motors
        self.camera = camera
        self.filesystem = filesystem
        
    def moveto(self, x, y):
        positions, speeds = self._compute_positions_and_speeds(x, y)
        for i in range(4):
            self.motors[i].moveto(positions[i], speeds[i])
        
    def grab(self):
        image = self.camera.grab()
        self.filesystem.store(image)

    def _compute_positions_and_speeds(self, x, y):
        current_positions = [self.motors[i].get_position() for i in range(4)]
        # ...
        #raise NotImplementedError # For Noé
        return [0, 0, 0, 0], [0.5, 0.5, 0.5, 0.5]
        
# Fake implementations

class FakeMotorController(IMotorController):    
    def __init__(self, maximum_position, maximum_speed):
        self.xmax = maximum_position
        self.vmax = maximum_speed
        
    def count_motors(self):
        2

    def get_motor(self, index):
        if index < 0 or index > 1:
              raise ValueError(f'Index out of bounds: {index}')
        return FakeMotor(0, self.xmax, self.vmax)

    
class FakeMotor(IMotor):
    def __init__(self, start_position, maximum_position, maximum_speed):
        self.x = start_position
        self.xmax = maximum_position
        self.vmax = maximum_speed
        
    def moveto(self, absolute_position, speed):
        if absolute_position < 0 or absolute_position > self.xmax:
              raise ValueError(f'Position out of bounds: {absolute_position}')
        if math.fabs(speed) > self.vmax:
              raise ValueError(f'Speed out of bounds: {speed}')
        self.x = absolute_position
        print(f'New position x={self.x}')

    def move(self, relative_distance, speed):
        self.moveto(self.x + relative_distance, speed)

    def get_position(self):
        return self.x


class FakeCamera(ICamera):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.counter = 0
    
    def grab(self):
        image = self._create_image()
        self._write_counter(image)
        return image

    def _create_image(self):
        return np.ones(shape=(self.height, self.width, 3), dtype=np.int8)

    def _write_counter(self, image):
        text = f'{self.counter:04d}'
        self.counter += 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1.5
        color = (255, 255, 255)
        thickness = 3
        image = cv2.putText(image, text, org, font,
                            fontScale, color, thickness, cv2.LINE_AA)
    
    
class FakeFilesystem(IFilesystem):    
    def store(self, image):
        print('Storing image')


# Default file system

class Filesystem(IFilesystem):
    def __init__(self, root_dir):
        self.root = root_dir
        self.counter = 0;
        
    def store(self, image):
        path = self._make_filepath()
        cv2.imwrite(path, image)
        print(f'Stored image {path}')
        
    def _make_filepath(self):
        filename = f'image-{self.counter:04d}.jpg'
        path = os.path.join(self.root, filename)
        self.counter += 1
        return path

# Odrive implementation
    
class OdriveBoard(IMotorController):    
    def __init__(self, serial_id):
        pass
              
    def count_motors(self):
        2

    def get_motor(self, index):
        pass
        
class OdriveMotor(IMotor):    
    def __init__(self, axis):
        self.axis = axis
              
    def moveto(self, absolute_position, speed):
        pass

    def move(self, relative_distance, speed):
        pass
        
    def get_position(self):
        pass
    
# Remote implementations

class RemoteCamera(ICamera):    
    def grab(self):
        pass

