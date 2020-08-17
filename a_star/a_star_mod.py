#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 03:06:19 2020

@author: prithvi
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class node():
    def __init__(self, h=0, g=0, f=0, cor=[0,0], b=[-1,-1]):
        self.h = h
        self.g = g
        self.f = f
        self.b = b
        self.cor = cor
        
def create_space(num_rows, num_cols, goal=[], obstacles=[], *args):
    """creates the space with the heuristics"""
    space = []
    for i in range (num_rows):
        space.append([])
    for i in range(num_rows):
        for j in range(num_cols):
            space[i].append([])
            
    for i in range(num_rows):
        for j in range(num_cols):
            space[i][j]=node()
            
    for i in range(num_rows):
        for j in range(num_cols):
            space[i][j].h = math.sqrt((goal[0]-i)**2 + (goal[1]-j)**2)
            space[i][j].f = 10000
            space[i][j].g = 10000
            
    for obs in obstacles:
        space[obs[0]][obs[1]].h = 1000
    
    heuristics = np.zeros((num_rows,num_cols))
    for i in range(num_rows):
        for j in range(num_cols):
            heuristics[i][j]=space[i][j].h
            
    for i in range(num_rows):
        for j in range(num_cols):
            space[i][j].cor = [i, j]
                            
    return space, heuristics

rows_dim = 10
cols_dim = 10
obstacles = [[8,1],[8,3],[8,9], [5,1], [0,1], [3,1], [2,2], [3,2], [4,3], [6,2], [6,3], [1,3], [0,5],
             [2,5], [3,5], [6,5], [7,6], [1,7], [3,7], [5,7], [2,8], [3,9], [4,9], [6,8],
             [7,8], [7,9], [6,4], [7,1], [6,1]]
goal=[0,9]
start=[9,0]

space, heuristics = create_space(rows_dim, cols_dim, goal, obstacles)


