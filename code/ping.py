# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 10:25:29 2022

@author: angab
"""

"""
Ce code permet de vérifier qu'un server répond à notre connection

"""

#version en True/False
import platform
import subprocess

def myping(host):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)

    if response == 0:
        return True
    else:
        return False
        
print(myping("www.google.com"))

#version en ms

from pythonping import ping

ping('10.100.3.2', verbose=True)