# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:07:38 2023

@author: angab
"""

import classe_mot_t as mo
import AntenneM as ant

if __name__=="__main__":
    #moteur=mo.FakeMotorT(10,5,0.5)
    moteur=mo.OdriveMot(10, 5, 0.5)
    antenne=ant.AntenneT(moteur,15555)
    init=input("Initialiser les moteurs? \n o - oui \n")
    if init=='o':
        antenne.init()
    antenne.run()