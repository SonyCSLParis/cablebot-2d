# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:00:40 2023

@author: angab
"""

import classe_mot_t as mo
import AntenneT as ant

if __name__=="__main__":
    moteur=mo.FakeMotorT(10,5,0.5)
    #moteur=mo.OdriveMot(10, 5, 0.5)
    antenne=ant.AntenneT(moteur,15558)
    antenne.run()