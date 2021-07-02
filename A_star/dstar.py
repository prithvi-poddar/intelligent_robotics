#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 15:01:31 2021

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt
from dstar_utilsutils import *
from astar import *

class Cell():
    def __init__(self, h=-1, k=-1, cor=[0,0], back=[-1,-1], t='NEW', is_obs = False):
        self.h = h
        self.k = k
        self.cor = cor
        self.back = back
        self.t = t
        self.is_obs = False

class Space():
    def __init__(self, num_rows, num_cols, num_obs, start, goal):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_obs = num_obs
        self.goal = goal
        self.start = start
        self.random_obstacle_generator()
        self.create_space()
        
    def random_obstacle_generator(self):
        count = 0
        self.obstacles = []
        while count != self.num_obs:
            x = np.random.randint(0, self.num_rows)
            y = np.random.randint(0, self.num_cols)
            if [x,y] not in self.obstacles and [x,y]!=self.goal and [x,y]!=self.start:
                count += 1
                self.obstacles.append([x,y])
                
    def create_space(self):
        self.space = []
        for i in range (self.num_rows):
            self.space.append([])
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.space[i].append([])
                
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.space[i][j] = Cell(cor=[i,j])
                
        for obs in self.obstacles:
            self.space[obs[0]][obs[1]].h = 10000
            self.space[obs[0]][obs[1]].is_obs = True
    
class D_star():
    def __init__(self, space, start, goal):
        self.space = space
        self.start = self.space[start[0]][start[1]]
        self.goal = self.space[goal[0]][goal[1]]
        
    def d_star(self):
        self.space[self.goal[0]][self.goal[1]].h = 0
        self.openList = [self.space[self.goal[0]][self.goal[1]]]
        self.Xc = self.space[self.start[0]][self.start[1]]
        self.Kmin = self.processState() ###################### takes openlist and space
        while(self.Kmin != -1 and self.Xc.t != 'CLOSED'):
            self.Kmin = self.processState()
        
        self.P = self.getBackPointerList() #####################takes space, Xc, goal state
        
        if(self.P == None):
            print("Goal not reachable")
            return 0
        
        while (self.Xc != self.start):
            neighbours = expand_node(self.space, self.Xc)
            for neighbour in neighbours:
                
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        