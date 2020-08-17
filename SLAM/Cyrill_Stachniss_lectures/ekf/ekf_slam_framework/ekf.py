#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:08:18 2020

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt
import math

class odom():
    def __init__(self, r1 = 0, t=0, r2 = 0):
        self.r1=r1
        self.r2=r2
        self.t=t
        
class sensor():
    def __init__(self, s1 = [0,0], s2 = [0,0], s3 = [0,0], s4 = [0,0], 
                 s5 = [0,0], s6 = [0,0], s7 = [0,0], s8 = [0,0], s9 = [0,0]):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.s5 = s5
        self.s6 = s6
        self.s7 = s7
        self.s8 = s8
        self.s9 = s9
        
def extract_data(datSensor):
    data=[]
    count = 0
    while True:
        u = odom()
        z = sensor()
        u.r1 = float(datSensor[count][1])
        u.t = float(datSensor[count][2])
        u.r2 = float(datSensor[count][3])
        sen_c = count+1
        while True:
            sensor_n = int(datSensor[sen_c][1]) 
            if sensor_n==1:
                z.s1=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==2:
                z.s2=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==3:
                z.s3=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==4:
                z.s4=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==5:
                z.s5=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==6:
                z.s6=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==7:
                z.s7=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==8:
                z.s8=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            elif sensor_n==9:
                z.s9=[float(datSensor[sen_c][2]), float(datSensor[sen_c][3])]
            
            sen_c = sen_c+1
            if sen_c==len(datSensor):
                break
            elif datSensor[sen_c][0]=='ODOMETRY':
                break
        
        count = sen_c
        data.append([u,z])
        if count==len(datSensor):
            break
    return data
    
datSensor = [i.strip().split() for i in open("data/sensor_data.dat").readlines()]
datWorld = [i.strip().split() for i in open("data/world.dat").readlines()]
data = extract_data(datSensor)


    