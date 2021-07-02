#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 20:13:02 2021

@author: prithvi
"""

from astar_utils import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def random_obstacle_generator(lim_row=10, lim_col=10, num=50, goal=[0,9], start=[9,0]):
    count = 0
    obstacles = []
    while count != num:
        x = np.random.randint(0, lim_row)
        y = np.random.randint(0, lim_col)
        if [x,y] not in obstacles and [x,y]!=goal and [x,y]!=start:
            count += 1
            obstacles.append([x,y])
    return obstacles

class A_star():
    def __init__(self, n_row=10, n_col=10, n_obs=5, start=[9,0], goal=[0,9]):
        self.n_row = n_row
        self.n_col = n_col
        self.n_obs = n_obs
        self.start = start
        self.goal = goal
        self.obstacles = random_obstacle_generator(lim_row=self.n_row, lim_col=self.n_col, num=self.n_obs,
                                                   goal=self.goal, start=self.start)
        self.space, self.heuristics = create_space(num_rows=self.n_row, num_cols=self.n_col, goal=self.goal, obstacles=self.obstacles)
        
    def generate_path(self):
        self.space[self.start[0]][self.start[1]].g = 0
        self.space[self.start[0]][self.start[1]].f = self.heuristics[self.start[0]][self.start[1]]
        
        self.open_set = []
        self.close_set = []
        
        self.open_set.append(self.space[self.start[0]][self.start[1]])
        self.path_found = False
        
        while (len(self.open_set)>0):
            n_best = find_best(self.open_set)
            if (n_best.cor == self.goal):
                self.path_found = True
                break
            
            pop_from_open(n_best, self.open_set, self.close_set)
            neighbours = expand_node(self.space, n_best)
            
            for neighbour in neighbours:
                tentative_g = n_best.g + dis(n_best, neighbour)
                if tentative_g < neighbour.g:
                    neighbour.back = n_best.cor
                    neighbour.g = tentative_g
                    neighbour.f = neighbour.g + neighbour.h
                    if neighbour not in self.open_set:
                        self.open_set.append(neighbour)
                        
        self.back_track()
                        
    def back_track(self):
        if (self.path_found == False):
            print("Goal is not reachable")
            
        else:
            self.x_b = self.goal[0]
            self.y_b = self.goal[1]   
            self.back_x = []
            self.back_y = []
            self.back_x.append(self.y_b+0.5)
            self.back_y.append(self.n_row-1-self.x_b+0.5)     
            while True:
                if [self.x_b, self.y_b]==self.start:
                    break
                x_temp = self.x_b
                y_temp = self.y_b
                self.x_b = self.space[x_temp][y_temp].back[0]
                self.y_b = self.space[x_temp][y_temp].back[1]
                self.back_x.append(self.y_b+0.5)
                self.back_y.append(self.n_row-1-self.x_b+0.5)
                
            print("Path found")
            
    def visualize(self):
        if (self.path_found == True):
            fig = plt.figure(figsize=(15, 10))
            ax = fig.gca()
            ax.set_xlim([0, self.n_row])
            ax.set_ylim([0, self.n_col])
            for ob in self.obstacles:
                x_bot = ob[1]
                y_bot = self.n_row-ob[0]-1
                rect = patches.Rectangle((x_bot,y_bot),1,1,linewidth=1,edgecolor='teal',facecolor='turquoise')
                ax.add_patch(rect)
            #ax.scatter(back_x, back_y)
            for cell in self.close_set:
                ax.scatter(cell.cor[1]+0.5, self.n_row-cell.cor[0]-0.5, color='grey', marker='o')
            ax.plot(self.back_x, self.back_y, color='black')
            ax.scatter(self.start[1]+0.5, self.n_row-self.start[0]-0.5, color='black', marker='x')
            ax.scatter(self.goal[1]+0.5, self.n_row-self.goal[0]-0.5, color='black', marker='o')
            plt.grid()
            plt.show()
        else:
            fig = plt.figure(figsize=(15, 10))
            ax = fig.gca()
            ax.set_xlim([0, self.n_row])
            ax.set_ylim([0, self.n_col])
            for ob in self.obstacles:
                x_bot = ob[1]
                y_bot = self.n_row-ob[0]-1
                rect = patches.Rectangle((x_bot,y_bot),1,1,linewidth=1,edgecolor='teal',facecolor='turquoise')
                ax.add_patch(rect)
            #ax.scatter(back_x, back_y)
            for cell in self.close_set:
                ax.scatter(cell.cor[1]+0.5, self.n_row-cell.cor[0]-0.5, color='grey', marker='o')
            ax.scatter(self.start[1]+0.5, self.n_row-self.start[0]-0.5, color='black', marker='x')
            ax.scatter(self.goal[1]+0.5, self.n_row-self.goal[0]-0.5, color='black', marker='o')
            plt.grid()
            plt.show()
            
