# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:51:53 2023

@author: angab
"""
from IPython import get_ipython
#get_ipython().magic('reset -sf')

import ClasseCam as ant

if __name__=="__main__":
    antenne=ant.AntenneCam(15559)
    antenne.run()
