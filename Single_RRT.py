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

for j in range(10000):
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
    new_node = [x_new,y_new]
    vertices.append(new_node)
  
    rand.append(qrand)
    plt.scatter(*zip(*vertices))
  
    