# -*- coding: utf-8 -*-
"""
Created on Fri May 26 14:48:25 2023

@author: angab
"""

import math
import time

kNord = [0, 0]
kOuest = [3, 0]
kEst = [0, 3]
kSud = [3, 3]
kDistancePerTurn = 0.075

def distance(a, b):
     dx = a[0] - b[0]
     dy = a[1] - b[1]
     return math.sqrt(dx * dx + dy * dy)

def unwind(reference, position, target):
     distance_start = distance(reference, position)
     distance_end = distance(reference, target)
     return distance_end - distance_start

def compute_unwind(position, target):
     nord = unwind(kNord, position, target)
     ouest = unwind(kOuest, position, target)
     est = unwind(kEst, position, target)
     sud = unwind(kSud, position, target)
     return [nord, ouest, est, sud]

def compute_turns(distances):
     return [distance / kDistancePerTurn for distance in distances]

def compute_speeds(turns, dt):
     return [turn / dt for turn in turns]

def compute_speeds_from_positions(position, target, dt):
     distances = compute_unwind(position, target)
     turns = compute_turns(distances)
     speeds = compute_speeds(turns, dt)
     return speeds

def estimate_new_position(position, dx):
     return [position[0] + dx[0], position[1] + dx[1]]

def sleep(dt):
     time.sleep(dt)

def pilot(speeds, dt):
     pass

def stop():
     pilot([0, 0, 0, 0], 1.0)

def compute_travel(position, target, duration, dt):
     dx = dt * (target[0] - position[0]) / duration
     dy = dt * (target[1] - position[1]) / duration
     return [dx, dy]

def travel(position, target, duration):
     speeds = compute_speeds_from_positions(position, target, duration)
     delta_t = 0.5 # seconds
     delta_x = compute_travel(position, target, duration, delta_t)
     while duration > 0:
         pilot(speeds, delta_t)
         sleep(delta_t)
         duration = duration - delta_t
         if duration > 0:
             next_position = estimate_new_position(position, delta_x)
             distances = compute_unwind(position, next_position)
             turns = compute_turns(distances)
             speeds = compute_speeds(turns, delta_t)
             position = next_position
             print(f'--\nPosition {position}\nDistances{distances}\nTurns {turns}\nSpeeds {speeds}')
         else:
             stop()

#a = [0, 0]
#b = [0, 1]

#travel(a, b, 10)
