# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:12:54 2023

@author: angab
"""

import socket

# Créer une instance de socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecter au serveur
client_socket.connect(('localhost',1555))

# Envoyer des données au serveur
client_socket.send("Hello, server!".encode())

# Recevoir des données du serveur
data = client_socket.recv(1024).decode()
print("Received data from server:", data)

# Fermer la connexion
client_socket.close()
