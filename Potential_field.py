#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:06:36 2021

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt


def grid_idx(grid_size, x, y):
    return int(int((grid_size-1)/2)-y), int(x+int((grid_size-1)/2))


def goal(d, theta, r, alpha, s):
    if (d<r):
        del_x = 0
        del_y = 0
        
    
    elif (d>=r and d<=s+r):
        del_x = -alpha * (d-r) * np.cos(theta)
        del_y = -alpha * (d-r) * np.sin(theta)
       
    
    else:
        del_x = -alpha * (s+r) * np.cos(theta)
        del_y = -alpha * (s+r) * np.sin(theta)

        
    return del_x, del_y


def obs(d, theta, r, beta, s):
    if (d<r):
        del_x = 0
        del_y = 0
        
    
    elif (d>=r and d<=s+r):
        del_x = beta * ((1/d)-(1/(s+r))) * np.cos(theta)
        del_y = beta * ((1/d)-(1/(s+r))) * np.sin(theta)
    
    else:
        del_x = 0
        del_y = 0
        
    return del_x, del_y

def make_space(limit):
    X = np.linspace(-limit, limit, (2*limit)+1)
    Y = np.linspace(-limit, limit, (2*limit)+1)
    return X, Y

X, Y = make_space(15)

goal_x, goal_y = 0, 0
r = 5
s = 15
alpha = 1
    
del_x = np.zeros((len(X), len(Y)))
del_y = np.zeros((len(X), len(Y)))

for i in range(len(X)):
    for j in range(len(Y)):
        dist = np.sqrt((X[i]-goal_x)**2 + (Y[j]-goal_y)**2)
        theta = np.arctan2((X[i]-goal_x), (Y[j]-goal_y))
        del_x[i][j], del_y[i][j] = goal(dist, theta, r, alpha, s)
            
    

figure, axes = plt.subplots() 
Drawing_colored_circle = plt.Circle(( 0, 0 ), r ) 
plt.quiver(X, Y, del_x, del_y)
axes.set_aspect( 1 ) 
axes.add_artist( Drawing_colored_circle )  
plt.show()


