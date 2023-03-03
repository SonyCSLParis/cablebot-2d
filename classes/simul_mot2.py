# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:53:26 2023

@author: angab
"""

import moteur_c as mot
import Remote_c as rem

vmax=10
cmax=3

if __name__=="__main__":
    moteur=mot.FakeMotor(10,3)
    remote=rem.RemoteMotor(moteur)
    
    ant=rem.Antenne(15556,remote)
    ant.run()