#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:48:12 2020

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt
import math

so = 10
ro = 10
sg = 10
rg = 1
x = 1
y = 1
locations = [[x,y]]
xg = 47
yg = 47
xo = 26
yo = 26
alpha = 2
beta = 7
dt = 0.01
for i in range(10000):
    dist_o = math.sqrt((x-xo)**2 + (y-yo)**2)
    dist_g = math.sqrt((x-xg)**2 + (y-yg)**2)
    theta_o = math.atan2(y-yo,x-xo)
    theta_g = math.atan2(y-yg,x-xg)
    
    if (dist_o<so+ro and dist_o>ro):
        uo = beta*(so+ro-dist_o)*math.cos(theta_o)
        vo = beta*(so+ro-dist_o)*math.sin(theta_o)
    elif (dist_o<=ro):
        uo = math.sign(math.cos(theta_o))*100
        vo = math.sign(math.sin(theta_o))*100
    else:
        uo = 0
        vo = 0
        
    if (dist_g<rg):
        ug = 0
        vg = 0
    elif (dist_g>=rg and dist_g<= sg+rg):
        ug = (-beta)*(dist_g-rg)*math.cos(theta_g)
        vg = (-beta)*(dist_g-rg)*math.sin(theta_g)
    else:
        ug = (-beta)*sg*math.cos(theta_g)
        vg = (-beta)*sg*math.sin(theta_g)
    if (dist_o <= ro):
        ug = 0
        vg = 0
        break;
        
    vx = ug+uo
    vy = vg+vo
    x = x + vx*dt
    y = y + vy*dt
    locations.append([x,y])
plt.scatter(*zip(*locations))