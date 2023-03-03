# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:25:26 2023

@author: angab
"""

import cv2
import os
from picamera import PiCamera
from time import sleep

class Camera:
    def __init__(self, name):
        self.name = name #nom de la caméra
        self.pic=0
        self.focus
    
    def raz(self):
        self.pic=0
    
    def newfocus(self,focus):
        self.focus=focus

class Camerabot(Camera):
    def __init__(self,name,focus):
        super().__init__(name,focus)
        self.cap=None
    
    def on(self):
        self.cap=PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        return True
    
    
    def takepic(self):
        self.pic=self.pic+1
        self.camera.capture('foo.jpg')
        print("L'image a été enregistrée avec succès")
        
    def off(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("caméra off")


class Fakecam(Camera):
    def __init__(self, name, path):
        super().__init__(name,1)
        self.cap=None
        self.Path=path
        
    def on(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("La caméra est inaccessible")
            return False
        else:
            return True
    
    def takepic(self):
        ret, frame = self.cap.read()
        if ret:
            self.pic=self.pic+1
            # Définir le nom de fichier et le chemin d'accès
            nom_fichier = "photo"+str(self.pic)+".jpg"
            chemin = self.Path

            # Vérifier si le dossier existe, sinon le créer
            if not os.path.exists(chemin):
                os.makedirs(chemin)

            # Enregistrer l'image dans le dossier spécifié
            cv2.imwrite(chemin + nom_fichier, frame)

            # Afficher un message de confirmation
            print("L'image a été enregistrée avec succès")
            return True
        else:
            return False
    
    def majpath(self,path):
        self.Path=path
        
    def off(self):
        self.cap.release()
        cv2.destroyAllWindows()






"""
# Créer un objet capture vidéo
cap = cv2.VideoCapture(0)

# Vérifier si la caméra est accessible
if not cap.isOpened():
    print("La caméra est inaccessible")
    exit()

# Capturer une image
ret, frame = cap.read()

# Si l'image est capturée avec succès
if ret:
    # Définir le nom de fichier et le chemin d'accès
    nom_fichier = "photo.jpg"
    chemin = "chemin/vers/le/dossier/"

    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(chemin):
        os.makedirs(chemin)

    # Enregistrer l'image dans le dossier spécifié
    cv2.imwrite(chemin + nom_fichier, frame)

    # Afficher un message de confirmation
    print("L'image a été enregistrée avec succès")

# Libérer la caméra et fermer la fenêtre
cap.release()
cv2.destroyAllWindows()
"""
"""
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture('foo.jpg')
"""