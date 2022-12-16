# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 15:35:36 2022

@author: angab
"""


#code de serveur pour communiquer
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))
#on attribue un port à notre serveur
socket.listen(5)
#5 connexions pendantes
client, address = socket.accept()
print ("{} connected".format( address ))
while True:
        response = client.recv(255)
        if response != "":
                print (response)

print ("Close")
client.close()
socket.close()