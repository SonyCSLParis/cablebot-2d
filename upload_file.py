import os
import sys
from googleapiclient.http import MediaFileUpload
from Google import Create_Service

#//!!!\\
#EN ARGV(ARGUMENT QUAND ON EXECUTE LE PROGRAMME)
#1: PATH VERS LE DOSSIER DE L'ORDI CONTENANT LES PHOTOS
#2: NOM DU DOSSIER A CREER DANS GOOGLE DRIVE QUI CONTIENDRA LES PHOTOS

# le Programme Crée un dossier dans google drive dont le nom est précisé en argv2,
# y envoie les photo dans le dossier dont le path est argv1, 
# puis supprime les photos du dossier de l'ordinateur.


CLIENT_SECRET_FILE = '/home/leonard/Documents/Projet indus/Google_drive_api/client_secret_cablecam.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

##folder_id = ['1j-ux1P75c6CYFBj0zi2YptP63YcQTA3l'] au cas ou on voudrait toujours envoyer au même dossier

file_names = os.listdir(sys.argv[1]) #nom du fichier à upload, peut etre une liste
k=0 
mime_types = []
for i in file_names:
    mime_types.append('image/png') #donner le mimetype pour chaque fichier dans le dossier (ici il n'y a que des png !!!!!)

file_metadata = {
        'name': sys.argv[2],
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
    file_name_directory = sys.argv[1]+ '/' + file_name

    media = MediaFileUpload(file_name_directory ,mimetype = mime_type)

    service.files().create(
        body = file_metadata,
        media_body = media,
        fields = 'id'
    ).execute() #envoi des photos



try:
    # Supprimer les fichiers du dossiers
    for i in file_names:
        os.remove(sys.argv[1]+'/'+i)
        print(f'Le fichier {i} a été supprimé avec succès.')
except OSError as e:
    print(f'Erreur lors de la suppression du fichier {file_names}: {e}')
