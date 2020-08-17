#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
circular obstacles at (2.5,2.5) and (4,3)
"""

import numpy as np
import math
import matplotlib.pyplot as plt


source = [1,1]
goal = [4.5,4.5]
xg = goal[0]
yg = goal[1]
delta = 0.01
edges = []
distances = [0]
vertices = [source]
count = 1
rand = []
n = 0

while (n<10000):
    qrand = [np.random.uniform(low=1.0, high = 5.1),np.random.uniform(low=1.0, high = 5.1)]
    x2 = qrand[0]
    y2 = qrand[1]
    length = len(vertices)
    distances=[]
    for i in range(length):
        x1 = vertices[i][0]
        y1 = vertices[i][1]
        dist = math.sqrt((x1-x2)**2 + (y2-y1)**2)
        distances.append(dist)
    
    k = np.argmin(distances)
    x1 = vertices[k][0]
    y1 = vertices[k][1]
    theta = math.atan2(y2-y1,x2-x1)
    x_new = x1 + delta*math.cos(theta)
    y_new = y1 + delta*math.sin(theta)
    if (math.sqrt((x_new-2.5)**2 + (y_new-2.5)**2) > 1 and math.sqrt((x_new-4)**2 + (y_new-3)**2) > 1):
        new_node = [x_new,y_new]
        vertices.append(new_node)
    #if (math.sqrt((x_new-xg)**2 + (y_new-yg)**2) <= 0.1):
     #   break
    n=n+1
    
circle1 = plt.Circle((2.5,2.5), 0.99, color='r')
circle2 = plt.Circle((4,3), 0.99, color='green')
fig, ax = plt.subplots()
tree = plt.scatter(*zip(*vertices))
ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(tree)
fig.show()
  
  