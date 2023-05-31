# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:38:31 2023

@author: angab
"""

from googleapiclient.http import MediaFileUpload
from Google import Create_Service
from datetime import date
from datetime import datetime
import socket
import testT as te
import time
import math
import os
from PIL import Image
import requests
from io import BytesIO
#import keyboard

class AntenneT:
    def __init__(self,mot,port):
        self.mot=mot
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        #on attribue un port à notre serveur
        self.socket.listen(5)
        #5 connexions pendantes
        self.client, self.address = self.socket.accept()
    
    def init(self):
        test=self.mot.set_config()
        if test==-1:
            print("ERREUR")
        return
    
    def run(self):
        print ("{} connected".format( self.address ))
        a=True
        self.mot.get()
        #print(self.mot.odrv)
        """ if test_mot < 0:
            print("erreur moteur non attaché")
            print ("Close")
            self.client.close()
            self.socket.close()
            return"""
        
        while a==True:
                mes = self.client.recv(255)
                mes=str(mes)
                if mes != "b''":
                    test=self.mot.run_m(mes)
                    print("test: ", test)
                    if test==False:
                        print("fermeture de serveur")
                        self.socket.settimeout(1)
                        a=False
                else:
                    a=False
        print ("Close")
        self.client.close()
        self.socket.close()
        return
    

class EmmeteurT:
    def __init__(self, host, port,turn):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tour=turn
        print("Attention, vérifiez bien qu'un couple positif enroule le câble")
        
    def connect(self):
        self.socket.connect((self.h, self.p))
        print ("Connection on {}".format(self.h))
        return
    
    def end(self):
        print ("Close")
        mes="END"
        self.socket.sendall(mes.encode())
        self.socket.close()
        return
        
    def pilote(self, val, T):
        mes="G "+str(val)+" "+str(T)
        print("message:",mes)
        self.socket.sendall(mes.encode())
        turn=val*T
        self.tour+=turn
        return
    
    def speed(self,v):
        mes="V "+str(v)
        self.socket.sendall(mes.encode())
        return
    
    def switch(self, mode):
        mes="S "+mode
        self.socket.sendall(mes.encode())
        return
    
    def set_tor(self,tor):
        mes="T "+str(tor)
        self.socket.sendall(mes.encode())
        
    def get_turn(self):
        return float(self.tour)
    
    def set_turn(self,turn):
        self.tour=turn
        return



"""
CLASSE MAJEUR DU PROJET
"""


class Cablebot:
    def __init__(self,Cam , Emet, long, larg, focus):#Rajouter la cam quand OK
        self.Cam=Cam
        self.Emet=Emet
        self.long=long
        self.larg=larg
        self.focus=focus
        self.Pos=None
        self.Tour=None
        self.conv=0.2
        
        #DATA
        self.kNord = [0, 0]
        self.kOuest = [3, 0]
        self.kEst = [0, 3]
        self.kSud = [3, 3]
        self.kDistancePerTurn = 0.1
    
    def start(self):
        if self.Cam != None:
            self.Cam.connect()
        for i in self.Emet:
            i.connect()
        time.sleep(20)
        self.Pos=te.calcul_pos(self.long,self.larg,self.focus)
        Tour=[]
        for i in self.Emet:
            Tour.append(i.get_turn())
        self.Tour=Tour
        return 0
    
    def add_emet(self,emet):
        if len(self.Emet)==4:
            print("Deja trop de moteurs")
            return -1
        else:
            self.Emet.append(emet)
            return 0
    
    def pic(self):
        self.Cam.takepic()
        return
    
    def endrun(self):
        self.Cam.finparc()
        return
    
    def set_torques(self,TOR):
        l=len(self.Emet)
        for i in range(l):
            self.Emet[i].set_tor(TOR[i])
        time.sleep(1)
        return
    
    def set_tour(self):
        Tour=[]
        for i in self.Emet:
            Tour.append(i.get_turn())
        self.Tour=Tour
        return 
    
    def quotidien(self):
        size=len(self.Emet)
        x=float(input("Quel x de départ? \n"))
        y=float(input("Quel y de départ? \n"))
        ORIGINE=te.calcul_long_mot([x,y],self.long,self.larg)
        
        #Definir le tour initial de chaque moteur 
        self.reset_mot(ORIGINE)
        
        for i in range(len(self.Pos)):
            
            #debugage
            print("\n")
            print('tour ',i,'du parcours')
            print("\n")
            
            
            #on recupere le point de l'étape
            Point=self.Pos[i]
            Cons,self.Tour=te.calcul_pos_mot(Point, self.long, self.larg, self.Tour)
            print("Cons: ",Cons)
            print("\n")
            Mod=[]
            for j in range(size):
                if Cons[j]>=0:
                    mode='t'
                    Cons[j]=-0.1
                else:
                    mode='v'
                Mod.append(mode)
            print("Mod: ",Mod,"\n")
            #MàJ des modes de chaque moteur
            self.switch(Mod)
            #time.sleep(1)
            
            Time=[]
            for k in Cons:
                t=te.calc_t(k)
                Time.append(t)
            T=Time[0]
            for i in range(1,size):
                if Time[i]>T:
                    T=Time[i]
            
            val1=Cons[0]
            if val1 !=-0.1:
                val1=te.calc_vit(T, val1)
                
            val2=Cons[1]
            if val2 !=-0.1:
                val2=te.calc_vit(T, val2)
                
            val3=Cons[2]
            if val3 !=-0.1:
                val3=te.calc_vit(T, val3)
                
            val4=Cons[3]
            if val4 !=-0.1:
                val4=te.calc_vit(T, val4)
                
            VAL=[val1,val2,val3,val4]
            for k in range(size):
                self.Emet[k].pilote(VAL[k],T)
            time.sleep(T)
            
            self.takepic()
        
        #self.endrun()
        return 0
    
    def goto(self, x, y):
        Point=[x,y]
        size=len(self.Emet)
        
        #definir la position d'origine
        x=float(input("Quel x de départ? \n"))
        y=float(input("Quel y de départ? \n"))
        ORIGINE=te.calcul_long_mot([x,y],self.long,self.larg)
        
        #Definir le tour initial de chaque moteur 
        self.reset_mot(ORIGINE)
        
        Cons,self.Tour=te.calcul_pos_mot(Point,self.long,self.larg,self.Tour)
        Mod=[]
        for i in range(size):
            if Cons[i]>=0:
                mode='t'
                Cons[i]=-0.1
            else:
                mode='v'
            Mod.append(mode)  
        self.switch(Mod)
        
        Time=[]
        for k in Cons:
            t=te.calc_t(k)
            Time.append(t)
        T=Time[0]
        for i in range(1,size):
            if Time[i]>T:
                T=Time[i]
        
        
        val1=Cons[0]
        if val1 !=-0.1:
            val1=te.calc_vit(T, val1)
           
        val2=Cons[1]
        if val2 !=-0.1:
            val2=te.calc_vit(T, val2)
           
        val3=Cons[2]
        if val3 != -0.1:
            val3=te.calc_vit(T, val3)
           
        val4=Cons[3]
        if val4 != -0.1:
            val4=te.calc_vit(T, val4)
           
        VAL=[val1,val2,val3,val4]
        for k in range(size):
            self.Emet[k].pilote(VAL[k],T)
        time.sleep(T)
        
        time.sleep(T)
        
        return 0
    
    def switch(self, Mode):
        l=len(self.Emet)
        T=[]
        V=[]
        for i in range(l):
            T.append('0')
            V.append('0')
        #print("T: ",T)
        #print("V: ",V)
        #print("\n")
        for i in range(l):
            mod=Mode[i]
            if mod=='t' or mod=='T':
                T[i]=mod
            else:
                V[i]=mod
        print("T': ",T)
        print("V': ",V)
        print("\n")
        
            
        for i in range(l):
            modt=T[i]
            #print("modt: ",modt)
            if modt!='0':    
                self.Emet[i].switch(modt)
            else:
                pass
        for i in range(l):
            modv=V[i]
            #print('modv: ',modv)
            #print("\n")
            if modv!='0':    
                self.Emet[i].switch(modv)
            else:
                pass
        time.sleep(1)
        return 0
    
    def takepic(self):
        for i in self.Emet:
            i.switch('v')
        time.sleep(1)
        #for i in self.Emet:
            #i.switch('v')
        #time.sleep(1)
        print("prise de photo")
        print("\n")
        if self.Cam != None:
            self.Cam.takepic()
        return 
        
    def end(self):
        print("SHUTDOWN")
        if self.Cam != None:
            self.Cam.end()
        for i in self.Emet:
            i.end()
    
    def reset_mot(self,L):
        for i in range(len(self.Emet)):
            turn=L[i]/self.conv
            self.Emet[i].set_turn(turn)
            self.set_tour()
    
    
    def speed(self,V):
        for i in range(len(self.Emet)):
            val=V[i]
            self.Emet[i].speed(val)
        time.sleep(1)
        
    def pilote(self, V, T):
        for i in range(len(self.Emet)):
            val=V[i]
            self.Emet[i].pilote(val,T)
        #time.sleep(0.5)
        
        return 0
    
    

    def distance(self,a, b):
         dx = a[0] - b[0]
         dy = a[1] - b[1]
         return math.sqrt(dx * dx + dy * dy)

    def unwind(self,reference, position, target):
         distance_start = self.distance(reference, position)
         distance_end = self.distance(reference, target)
         return distance_end - distance_start

    def compute_unwind(self,position, target):
         nord = self.unwind(self.kNord, position, target)
         ouest = self.unwind(self.kOuest, position, target)
         est = self.unwind(self.kEst, position, target)
         sud = self.unwind(self.kSud, position, target)
         return [nord, ouest, est, sud]

    def compute_turns(self,distances):
         return [distance / self.kDistancePerTurn for distance in distances]

    def compute_speeds(self,turns, dt):
         return [turn / dt for turn in turns]

    def compute_speeds_from_positions(self,position, target, dt):
         distances = self.compute_unwind(position, target)
         turns = self.compute_turns(distances)
         speeds = self.compute_speeds(turns, dt)
         return speeds

    def estimate_new_position(self,position, dx):
         return [position[0] + dx[0], position[1] + dx[1]]

    def sleep(self,dt):
         time.sleep(dt)


    def stop(self):
         self.pilote([0, 0, 0, 0], 1.0)

    def compute_travel(self,position, target, duration, dt):
         dx = dt * (target[0] - position[0]) / duration
         dy = dt * (target[1] - position[1]) / duration
         return [dx, dy]

    def travel(self,position, target, duration):
        speeds = self.compute_speeds_from_positions(position, target, duration)
        print("speeds initiales: ",speeds)
        Mod=[]
        x=target[0]
        y=target[1]
        S_dead=0 # start dead zone
        E_dead=0.8 #end dead zone
        if S_dead <= x <= E_dead or S_dead <= y <= E_dead:
            tor=-0.05
        else:
            tor=-0.1
        TOR=[tor,tor,tor,tor]
        self.set_torques(TOR)
        for i in range (4):
            if speeds[i]<0:
                mod='v'
            else:
                mod='t'
            Mod.append(mod)
        print("Mod initial: ",Mod)
        self.switch(Mod)
        #time.sleep(1)
        delta_t = 2 # seconds
        delta_x = self.compute_travel(position, target, duration, delta_t)
        j=0
        while duration > 0:
            #if keyboard.is_pressed('space'):
                #self.speed([0,0,0,0])
               # break
            self.pilote(speeds, delta_t)
            self.sleep(1)
            duration = duration - delta_t
            if duration > 0:
                next_position = self.estimate_new_position(position, delta_x)
                distances = self.compute_unwind(position, next_position)
                turns = self.compute_turns(distances)
                speeds = self.compute_speeds(turns, delta_t)
                print("speeds ",j," : ",speeds)
                Mod=[]
                for i in range (4):
                    if speeds[i]<0:
                        mod='v'
                    else:
                        mod='t'
                    Mod.append(mod)
                print("Mod ",i,"")
                self.switch(Mod)
                position = next_position
                print(f'--\nPosition {position}\nDistances{distances}\nTurns {turns}\nSpeeds {speeds}')
            else:
                self.stop()
                j+=1
    """
    fonction temporaire pour tester la 2D
    """
    def plan_test(self):
        Cons=te.pos_plan()
        T=10
        for i in range(1,len(Cons)):
            pt_start=Cons[i-1]
            pt_goal=Cons[i]
            self.travel(pt_start,pt_goal,T)
            self.takepic()
            self.recup_image()
        return 0



class EmmetCam:
    def __init__(self, host, port):
        self.h=host
        self.p=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.compteur=0
        
    def connect(self):
        self.socket.connect((self.h, self.p))
        print ("Connection on {}".format(self.h))
        return        
    
    def takepic(self):
        mes_pic='pic'
        self.socket.sendall(mes_pic.encode())
        time.sleep(10)
        self.compteur+=1
        self.recup_image(self.compteur)
        return
    
    def finparc(self):
        #mes='1'
        print("Fin de parcours") 
        path = "Users/angab/OneDrive/Documents/ROB4/PI/photos/"
        now = datetime.now()
        print("now: ",now)
        current_time = str(now.strftime("%H:%M:%S"))
        print("current_time", current_time)
        self.uploadFile(path, current_time)
        #self.socket.sendall(mes.encode())
        
        time.sleep(5)
        return
    
    def end(self):
        mes_end='E'
        print("Fermeture camera")
        self.socket.sendall(mes_end.encode())
        self.socket.close()
        print("Caméra déconnectée")
        return
        
    def recup_image(self, count): 
        url = "https://192.168.1.184" 
        name = str(count) + ".png" 
        response = requests.get(url) 
        img = Image.open(BytesIO(response.content)) 
        chemin_destination = "Users/angab/OneDrive/Documents/ROB4/PI/photos/" + name 
        nom_fichier = str(self.compteur) 
        img.save(chemin_destination + nom_fichier) 
        print("L'image a été enregistrée avec succès.")
        return
		
    def upload_file(self, path, name):
        """!
        Cette fonction permet de créer un dossier dans Google Drive avec le nom indiqué en parametre et d'envoyer des photos enregistrés localement depuis le path indiqué vers le dossier créé. Supprime en suite les photos du dossier local. 
        @param path chemin du dossier local contenant les photos 
        @param name nom du dossier à créer dans Google Drive
        """
    	        #//!!!\\
        #EN ARGV(ARGUMENT QUAND ON EXECUTE LE PROGRAMME)
        #1: PATH VERS LE DOSSIER DE L'ORDI CONTENANT LES PHOTOS
        #2: NOM DU DOSSIER A CREER DANS GOOGLE DRIVE QUI CONTIENDRA LES PHOTOS

        # le Programme Crée un dossier dans google drive dont le nom est précisé en argv2,
        # y envoie les photo dans le dossier dont le path est argv1, 
        # puis supprime les photos du dossier de l'ordinateur.

        print("Début d'envoi")
        CLIENT_SECRET_FILE = 'Users/angab/OneDrive/Documents/ROB4/PI/code/cablebot-2d/classes/classes_v2/client_secret_cablecam.json'#'/home/pi/cablebot/classes/classes_v2/client_secret_cablecam.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        ##folder_id = ['1j-ux1P75c6CYFBj0zi2YptP63YcQTA3l'] au cas ou on voudrait toujours envoyer au même dossier 
        file_names = os.listdir(path) #nom du fichier à upload, peut etre une liste
        #k=0 
        mime_types = []
        for i in file_names:
            mime_types.append('image/png') #donner le mimetype pour chaque fichier dans le dossier (ici il n'y a que des png !!!!!)
            print("nametype de",i)
        file_metadata = {
                'name': name,
                'mimeType' : 'application/vnd.google-apps.folder',
                
            }

        folder_id = [service.files().create(body = file_metadata, fields='id').execute()['id']] #Creation du dossier dans google drive 
                                                                                                #et récupération du folder ID pour 
        print(folder_id)                                                                        #ensuite envoyer les photos dans ce dossier
        for file_name, mime_type in zip(file_names, mime_types):
            print("file name")
            print(file_name)
            print("\n")
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
        
        print("fin d'envoi")
        return
			
        
