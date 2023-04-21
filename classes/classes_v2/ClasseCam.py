# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:38:31 2023

@author: angab
"""

import os
import socket
import time
from time import sleep
from picamera import PiCamera
import os
import sys
from googleapiclient.http import MediaFileUpload
from Google import Create_Service
from datetime import date
from datetime import datetime





class AntenneCam:
    def __init__(self,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        #on attribue un port à notre serveur
        self.socket.listen(5)
        #5 connexions pendantes
        self.client, self.address = self.socket.accept()
        
    def run(self):
        print ("{} connected".format( self.address ))
        a=True
        count = 0
        while a==True:
                count = count +1
                
                mes = self.client.recv(255)
                mes=str(mes)
                if mes != "b''":
                    
                    valeur = mes[2]

                    if (valeur == 1):
                        path = '/home/pi/photopicam/'
                        #today = date.today() version finale avec la date, version test avec heure
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        self.uploadFile(path, current_time)
                    else:
                        self.prendrePhoto(count)
                else:
                    a=False
        print ("Close")
        self.client.close()
        self.socket.close()
        return
    
    def prendrePhoto(self, a):
        # Ce programme prend une photo avec la picamera, les enregistre dans le path indique dans le programme.
        # Le detail du nom doit etre precise en argv1 de sorte a ce que une nouvelle photo soit cree au lieu de modifier celle d'avant

        file_path = '/home/pi/photopicam/photo_picamera' + str(a) + '.png'
        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(0.5)
        camera.capture(file_path)
        print("prise de photo")
        camera.stop_preview()
        sleep(0.5)
        camera.close() 
        return
    
    def uploadFile(self, path, name):
        #//!!!\\
        #EN ARGV(ARGUMENT QUAND ON EXECUTE LE PROGRAMME)
        #1: PATH VERS LE DOSSIER DE L'ORDI CONTENANT LES PHOTOS
        #2: NOM DU DOSSIER A CREER DANS GOOGLE DRIVE QUI CONTIENDRA LES PHOTOS

        # le Programme Crée un dossier dans google drive dont le nom est précisé en argv2,
        # y envoie les photo dans le dossier dont le path est argv1, 
        # puis supprime les photos du dossier de l'ordinateur.


        CLIENT_SECRET_FILE = '/home/pi/cablebot/classes/classes_v2/client_secret_cablecam.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        ##folder_id = ['1j-ux1P75c6CYFBj0zi2YptP63YcQTA3l'] au cas ou on voudrait toujours envoyer au même dossier

        file_names = os.listdir(path) #nom du fichier à upload, peut etre une liste
        k=0 
        mime_types = []
        for i in file_names:
            mime_types.append('image/png') #donner le mimetype pour chaque fichier dans le dossier (ici il n'y a que des png !!!!!)

        file_metadata = {
                'name': name,
                'mimeType' : 'application/vnd.google-apps.folder',
                
            }

        folder_id = [service.files().create(body = file_metadata, fields='id').execute()['id']] #Creation du dossier dans google drive 
                                                                                                #et récupération du folder ID pour 
        print(folder_id)                                                                        #ensuite envoyer les photos dans ce dossier
        for file_name, mime_type in zip(file_names, mime_types):
            print(file_name)
            file_metadata = {
                'name' : file_name,
                'parents' : folder_id
            }
            file_name_directory = path + '/' + file_name

            media = MediaFileUpload(file_name_directory ,mimetype = mime_type)

            service.files().create(
                body = file_metadata,
                media_body = media,
                fields = 'id'
            ).execute() #envoi des photos



        try:
            # Supprimer les fichiers du dossiers
            for i in file_names:
                os.remove(path +'/'+i)
                print(f'Le fichier {i} a été supprimé avec succès.')
        except OSError as e:
            print(f'Erreur lors de la suppression du fichier {file_names}: {e}')
    
