# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 09:26:10 2022

@author: angab
"""
import time
  
#fonction de compte à rebours
def countdown(t):
    #convertir t en secondes
    t=t*24*60*60
    while t:
        #determiner le temps
        secondes = t
        heures, secondes = divmod(secondes, 3600)
        minutes, secondes = divmod(secondes, 60)
        timer= str(heures)+ ":"+str(minutes)+":"+str(secondes)
        #affichage du temps avant lancement
        print(timer, end='\r')
        print('',end='\r',flush=True)
        time.sleep(1)
        print('',end='\r',flush=True)
        t -= 1
      
    print('Fire in the hole!!')
  
#choix de l'utilisateur du temps avant prochain passage
t = input("Enter the number of days between every run: ")
  
# function call
countdown(int(t))