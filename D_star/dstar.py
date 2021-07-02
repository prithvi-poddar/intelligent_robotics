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
            return None
        
        while (self.Xc != self.goal):
            neighbours = expand_node(self.space, self.Xc)
            for neighbour in neighbours:
                temp_start = self.Xc.corr
                temp_goal = neighbour.cor
                temp = A_star(n_row=len(self.space) , n_col=len(self.space), start=temp_start, goal=temp_goal, obstacles=self.space.obstacles)
                temp.generate_path()
                r = temp.get_cost()
                if (neighbour.is_obs == True):
                    self.Kmin = self.modifyCost(self.Xc, neighbour, r) ######################### takes open, Xc, neigh, r
                    
                    while(self.Kmin<=self.Xc.h and self.Kmin != -1):
                        self.Kmin = self.processState()
                    self.P = self.getBackPointerList()
                    if(self.P == None):
                        print("Goal not reachable")
                        return None
                    
            self.Xc = self.P[1]
            self.P = self.getBackPointerList()
        return self.Xc
    
    def getBackPointerList(self):
        pass
    
    def insert(self, cell, hnew):
        if(cell.t == 'NEW'):
            cell.k = hnew
        elif(cell.t == 'OPEN'):
            cell.k = min(cell.k, hnew)
        elif(cell.t == 'CLOSED'):
            cell.k = min(cell.h, hnew)
            
        cell.h = hnew
        cell.t = 'OPEN'
        
    def modifyCost(self, X, Y, cval):
        if(X.t == 'CLOSED'):
            self.insert(X, X.h)
        return self.getKmin()
    
    def getKmin(self):
        if(len(self.openList) == 0):
            return -1
        else:
            mink=1000000
            for a in self.openList:
                if(a.k < mink):
                    mink = a.k
            return mink
        
    def minState(self):
        if(len(self.openList) == 0):
            return -1
        else:
            mink=self.openList[0]
            for a in self.openList:
                if(a.k < mink.k):
                    mink = a
            return mink

    def processState(self):
        X = self.minState()
        if (X == -1):
            return (-1)
        kold = self.getKmin()
        if (kold < X.h):
            for Y in expand_node(self.space, X):
                c = np.sqrt((Y.cor[0]-X.cor[0])**2 + (Y.cor[1]-X.cor[1])**2)
                if (Y.is_obs == True):
                    c = 10000
                if (Y.h < kold and X.h > Y.h + c):
                    X.back = Y.cor
                    X.h = Y.h + c
                    
        elif(kold == X.h):
            for Y in expand_node(self.space, X):
                c = np.sqrt((Y.cor[0]-X.cor[0])**2 + (Y.cor[1]-X.cor[1])**2)
                if (Y.is_obs == True):
                    c = 10000
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        