# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:10:08 2023

@author: angab
"""

import AntenneT as ant
from IPython import get_ipython
get_ipython().magic('reset -f')

hostcam = '192.168.1.141'
portcam = 15555

input("pause")

try:
    cam = ant.EmmetCam(hostcam, portcam)
    cam.connect()
    for i in range(5):
        cam.takepic()
    cam.finparc()
    cam.end()
except BaseException as e:
    cam.end()
    print("Erreur :", e)