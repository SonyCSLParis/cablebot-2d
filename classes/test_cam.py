# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:22:04 2023

@author: angab
"""
import cv2
import os

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
    chemin = "C:\\Users\\angab\\OneDrive\\Documents\\ROB4\\PI\\code\\odrive\\classes\\img_test\\"

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