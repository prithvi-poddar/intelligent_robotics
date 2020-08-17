#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:09:30 2020

@author: prithvi
"""

import numpy as np
import math
import matplotlib.pyplot as plt

np.random.seed(3)
source = [1,1,0]
"""
goal = [4.5,4.5]
xg = goal[0]
yg = goal[1]
"""
delta = 0.01
#edges = []

vertices = [source]
link = [[0,0,0]]
while True:
    qrand = qrand = [np.random.uniform(low=1.0, high = 5.1),np.random.uniform(low=1.0, high = 5.1)]
    xrand = qrand[0]
    yrand = qrand[1]
    weight = math.sqrt((vertices[0][0]-xrand)**2 + (vertices[0][1]-yrand)**2)
    if (weight<=1):
        vertices.append([xrand,yrand,weight])
        link.append(vertices[0])
        break

for j in range(5000):
    qrand = [np.random.uniform(low=1.0, high = 5.1),np.random.uniform(low=1.0, high = 5.1)]
    xrand = qrand[0]
    yrand = qrand[1]
    allowed_vertices = []
    count=0
    for i in range (len(vertices)):
        distance = math.sqrt((vertices[i][0]-xrand)**2 + (vertices[i][1]-yrand)**2)
        if(distance<=1):
            allowed_vertices.append(1)
        else:
            allowed_vertices.append(0)
            count=count+1
            
    if (count<len(vertices)):
        distances = []
        for i in range(len(vertices)):
            if (allowed_vertices[i]==1):
                distances.append(math.sqrt((vertices[i][0]-xrand)**2 + (vertices[i][1]-yrand)**2))
            else:
                distances.append(1000)
        to_link = np.argmin(distances)
        vertices.append([xrand,yrand,vertices[to_link][2]+math.sqrt((vertices[to_link][0]-xrand)**2 + (vertices[to_link][1]-yrand)**2)])
        link.append(vertices[to_link])


   
for i in range(1,len(vertices)):
    point1 = [link[i][0],link[i][1]]
    point2 = [vertices[i][0],vertices[i][1]]
    
    x_val = [point1[0],point2[0]]
    y_val = [point1[1],point2[1]]
    
    plt.plot(x_val,y_val,color='blue')

