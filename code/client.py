# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 15:36:43 2022

@author: angab
"""
#code client pour communiquer

import socket

hote = "localhost"
port = 15555
b=int (1)

#initialisation de la socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print ("Connection on {}".format(port))
while b==1:
    mes=input("Entrez vôtre message\n")
    socket.send(mes.encode())

    b=int(input("Nouveau message?\n 1=oui 0= non\n"))

#sortie de boucle donc fermeture de la socket
print ("Close")
socket.close()

