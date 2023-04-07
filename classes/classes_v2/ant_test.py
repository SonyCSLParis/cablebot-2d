# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:51:53 2023

@author: angab
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')
import classe_mot_t as mo
import AntenneT as ant

if __name__=="__main__":
    #moteur=mo.FakeMotorT(10,3,0,"Le moteur de Nono")
    moteur=mo.OdriveMot(5, 5, 0.5)
    antenne=ant.AntenneT(moteur,15555)
    antenne.run()