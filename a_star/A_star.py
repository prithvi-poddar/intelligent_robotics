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

def find_best(open_list):
    mini = open_list[0]
    n = len(open_list)
    for i in range(1, n):
        if open_list[i].f<mini.f:
            mini = open_list[i]
    return mini

def cal_g(node, node_):
    x1 = node.cor[0]
    y1 = node.cor[1]
    x2 = node_.cor[0]
    y2 = node_.cor[1]
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    g = dist + node.g
    return g


def expand_node(space, node, opened, closed):
    lim_row = len(space)-1
    lim_col = len(space[0])-1
    row = node.cor[0]
    col = node.cor[1]
    
    if row+1<=lim_row and col+1<=lim_col and row-1>=0 and col-1>=0:
        
        if space[row+1][col+1] not in opened and space[row+1][col+1] not in closed and space[row+1][col+1].h!=1000:
            opened.append(space[row+1][col+1])  
            space[row+1][col+1].g = cal_g(node, space[row+1][col+1])
            space[row+1][col+1].f = space[row+1][col+1].h + space[row+1][col+1].g
            space[row+1][col+1].b = [row, col]
            
        if space[row][col+1] not in opened and space[row][col+1] not in closed and space[row][col+1].h!=1000:
            opened.append(space[row][col+1]) 
            space[row][col+1].g = cal_g(node, space[row][col+1])
            space[row][col+1].f = space[row][col+1].h + space[row][col+1].g
            space[row][col+1].b = [row, col]
            
        if space[row+1][col] not in opened and space[row+1][col] not in closed and space[row+1][col].h!=1000:
            opened.append(space[row+1][col]) 
            space[row+1][col].g = cal_g(node, space[row+1][col])
            space[row+1][col].f = space[row+1][col].h + space[row+1][col].g
            space[row+1][col].b = [row, col]
            
        if space[row-1][col-1] not in opened and space[row-1][col-1] not in closed and space[row-1][col-1].h!=1000:
            opened.append(space[row-1][col-1]) 
            space[row-1][col-1].g = cal_g(node, space[row-1][col-1])
            space[row-1][col-1].f = space[row-1][col-1].h + space[row-1][col-1].g
            space[row-1][col-1].b = [row, col]
            
        if space[row-1][col] not in opened and space[row-1][col] not in closed and space[row-1][col].h!=1000:
            opened.append(space[row-1][col])  
            space[row-1][col].g = cal_g(node, space[row-1][col])
            space[row-1][col].f = space[row-1][col].h + space[row-1][col].g
            space[row-1][col].b = [row, col]
            
        if space[row][col-1] not in opened and space[row][col-1] not in closed and space[row][col-1].h!=1000:
            opened.append(space[row][col-1])  
            space[row][col-1].g = cal_g(node, space[row][col-1])
            space[row][col-1].f = space[row][col-1].h + space[row][col-1].g
            space[row][col-1].b = [row, col]
            
        if space[row-1][col+1] not in opened and space[row-1][col+1] not in closed and space[row-1][col+1].h!=1000:
            opened.append(space[row-1][col+1]) 
            space[row-1][col+1].g = cal_g(node, space[row-1][col+1])
            space[row-1][col+1].f = space[row-1][col+1].h + space[row-1][col+1].g
            space[row-1][col+1].b = [row, col]
            
        if space[row+1][col-1] not in opened and space[row+1][col-1] not in closed and space[row+1][col-1].h!=1000:
            opened.append(space[row+1][col-1])
            space[row+1][col-1].g = cal_g(node, space[row+1][col-1])
            space[row+1][col-1].f = space[row+1][col-1].h + space[row+1][col-1].g
            space[row+1][col-1].b = [row, col]
            
                
    elif row==0 and col==0:
        if space[row+1][col+1] not in opened and space[row+1][col+1] not in closed and space[row+1][col+1].h!=1000:
            opened.append(space[row+1][col+1])  
            space[row+1][col+1].g = cal_g(node, space[row+1][col+1])
            space[row+1][col+1].f = space[row+1][col+1].h + space[row+1][col+1].g
            space[row+1][col+1].b = [row, col]
            
        if space[row][col+1] not in opened and space[row][col+1] not in closed and space[row][col+1].h!=1000:
            opened.append(space[row][col+1]) 
            space[row][col+1].g = cal_g(node, space[row][col+1])
            space[row][col+1].f = space[row][col+1].h + space[row][col+1].g
            space[row][col+1].b = [row, col]
            
        if space[row+1][col] not in opened and space[row+1][col] not in closed and space[row+1][col].h!=1000:
            opened.append(space[row+1][col])
            space[row+1][col].g = cal_g(node, space[row+1][col])
            space[row+1][col].f = space[row+1][col].h + space[row+1][col].g
            space[row+1][col].b = [row, col]
            
        
    elif row==0 and col==lim_col:
        if space[row+1][col] not in opened and space[row+1][col] not in closed and space[row+1][col].h!=1000:
            opened.append(space[row+1][col])  
            space[row+1][col].g = cal_g(node, space[row+1][col])
            space[row+1][col].f = space[row+1][col].h + space[row+1][col].g
            space[row+1][col].b = [row, col]
            
        if space[row][col-1] not in opened and space[row][col-1] not in closed and space[row][col-1].h!=1000:
            opened.append(space[row][col-1])
            space[row][col-1].g = cal_g(node, space[row][col-1])
            space[row][col-1].f = space[row][col-1].h + space[row][col-1].g
            space[row][col-1].b = [row, col]
            
        if space[row+1][col-1] not in opened and space[row+1][col-1] not in closed and space[row+1][col-1].h!=1000:
            opened.append(space[row+1][col-1])
            space[row+1][col-1].g = cal_g(node, space[row+1][col-1])
            space[row+1][col-1].f = space[row+1][col-1].h + space[row+1][col-1].g
            space[row+1][col-1].b = [row, col]
            
        
    elif row==lim_row and col==0:
        if space[row-1][col] not in opened and space[row-1][col] not in closed and space[row-1][col].h!=1000:
            opened.append(space[row-1][col])
            space[row-1][col].g = cal_g(node, space[row-1][col])
            space[row-1][col].f = space[row-1][col].h + space[row-1][col].g
            space[row-1][col].b = [row, col]
            
        if space[row][col+1] not in opened and space[row][col+1] not in closed and space[row][col+1].h!=1000:
            opened.append(space[row][col+1])
            space[row][col+1].g = cal_g(node, space[row][col+1])
            space[row][col+1].f = space[row][col+1].h + space[row][col+1].g
            space[row][col+1].b = [row, col]
            
        if space[row-1][col+1] not in opened and space[row-1][col+1] not in closed and space[row-1][col+1].h!=1000:
            opened.append(space[row-1][col+1])
            space[row-1][col+1].g = cal_g(node, space[row-1][col+1])
            space[row-1][col+1].f = space[row-1][col+1].h + space[row-1][col+1].g
            space[row-1][col+1].b = [row, col]
            
        
    elif row==lim_row and col==lim_col:
        if space[row-1][col-1] not in opened and space[row-1][col-1] not in closed and space[row-1][col-1].h!=1000:
            opened.append(space[row-1][col-1])
            space[row-1][col-1].g = cal_g(node, space[row-1][col-1])
            space[row-1][col-1].f = space[row-1][col-1].h + space[row-1][col-1].g
            space[row-1][col-1].b = [row, col]
            
        if space[row-1][col] not in opened and space[row-1][col] not in closed and space[row-1][col].h!=1000:
            opened.append(space[row-1][col])
            space[row-1][col].g = cal_g(node, space[row-1][col])
            space[row-1][col].f = space[row-1][col].h + space[row-1][col].g
            space[row-1][col].b = [row, col]
            
        if space[row][col-1] not in opened and space[row][col-1] not in closed and space[row][col-1].h!=1000:
            opened.append(space[row][col-1])
            space[row][col-1].g = cal_g(node, space[row][col-1])
            space[row][col-1].f = space[row][col-1].h + space[row][col-1].g
            space[row][col-1].b = [row, col]
            
        
    elif row==0 and 0<col and col<lim_col:
        if space[row][col-1] not in opened and space[row][col-1] not in closed and space[row][col-1].h!=1000:
            opened.append(space[row][col-1])
            space[row][col-1].g = cal_g(node, space[row][col-1])
            space[row][col-1].f = space[row][col-1].h + space[row][col-1].g
            space[row][col-1].b = [row, col]
            
        if space[row+1][col-1] not in opened and space[row+1][col-1] not in closed and space[row+1][col-1].h!=1000:
            opened.append(space[row+1][col-1])
            space[row+1][col-1].g = cal_g(node, space[row+1][col-1])
            space[row+1][col-1].f = space[row+1][col-1].h + space[row+1][col-1].g
            space[row+1][col-1].b = [row, col]
            
        if space[row+1][col] not in opened and space[row+1][col] not in closed and space[row+1][col].h!=1000:
            opened.append(space[row+1][col])
            space[row+1][col].g = cal_g(node, space[row+1][col])
            space[row+1][col].f = space[row+1][col].h + space[row+1][col].g
            space[row+1][col].b = [row, col]
            
        if space[row+1][col+1] not in opened and space[row+1][col+1] not in closed and space[row+1][col+1].h!=1000:
            opened.append(space[row+1][col+1])
            space[row+1][col+1].g = cal_g(node, space[row+1][col+1])
            space[row+1][col+1].f = space[row+1][col+1].h + space[row+1][col+1].g
            space[row+1][col+1].b = [row, col]
            
        if space[row][col+1] not in opened and space[row][col+1] not in closed and space[row][col+1].h!=1000:
            opened.append(space[row][col+1])
            space[row][col+1].g = cal_g(node, space[row][col+1])
            space[row][col+1].f = space[row][col+1].h + space[row][col+1].g
            space[row][col+1].b = [row, col]
            
        
    elif 0<row<lim_row and col==lim_col:
        if space[row-1][col] not in opened and space[row-1][col] not in closed and space[row-1][col].h!=1000:
            opened.append(space[row-1][col])
            space[row-1][col].g = cal_g(node, space[row-1][col])
            space[row-1][col].f = space[row-1][col].h + space[row-1][col].g
            space[row-1][col].b = [row, col]
            
        if space[row-1][col-1] not in opened and space[row-1][col-1] not in closed and space[row-1][col-1].h!=1000:
            opened.append(space[row-1][col-1])
            space[row-1][col-1].g = cal_g(node, space[row-1][col-1])
            space[row-1][col-1].f = space[row-1][col-1].h + space[row-1][col-1].g
            space[row-1][col-1].b = [row, col]
            
        if space[row][col-1] not in opened and space[row][col-1] not in closed and space[row][col-1].h!=1000:
            opened.append(space[row][col-1])
            space[row][col-1].g = cal_g(node, space[row][col-1])
            space[row][col-1].f = space[row][col-1].h + space[row][col-1].g
            space[row][col-1].b = [row, col]
            
        if space[row+1][col-1] not in opened and space[row+1][col-1] not in closed and space[row+1][col-1].h!=1000:
            opened.append(space[row+1][col-1])
            space[row+1][col-1].g = cal_g(node, space[row+1][col-1])
            space[row+1][col-1].f = space[row+1][col-1].h + space[row+1][col-1].g
            space[row+1][col-1].b = [row, col]
            
        if space[row+1][col] not in opened and space[row+1][col] not in closed and space[row+1][col].h!=1000:
            opened.append(space[row+1][col])
            space[row+1][col].g = cal_g(node, space[row+1][col])
            space[row+1][col].f = space[row+1][col].h + space[row+1][col].g
            space[row+1][col].b = [row, col]
            
        
    elif row==lim_row and 0<col and col<lim_col:
        if space[row][col-1] not in opened and space[row][col-1] not in closed and space[row][col-1].h!=1000:
            opened.append(space[row][col-1])
            space[row][col-1].g = cal_g(node, space[row][col-1])
            space[row][col-1].f = space[row][col-1].h + space[row][col-1].g
            space[row][col-1].b = [row, col]
            
        if space[row-1][col-1] not in opened and space[row-1][col-1] not in closed and space[row-1][col-1].h!=1000:
            opened.append(space[row-1][col-1])
            space[row-1][col-1].g = cal_g(node, space[row-1][col-1])
            space[row-1][col-1].f = space[row-1][col-1].h + space[row-1][col-1].g
            space[row-1][col-1].b = [row, col]
            
        if space[row-1][col] not in opened and space[row-1][col] not in closed and space[row-1][col].h!=1000:
            opened.append(space[row-1][col])
            space[row-1][col].g = cal_g(node, space[row-1][col])
            space[row-1][col].f = space[row-1][col].h + space[row-1][col].g
            space[row-1][col].b = [row, col]
            
        if space[row-1][col+1] not in opened and space[row-1][col+1] not in closed and space[row-1][col+1].h!=1000:
            opened.append(space[row-1][col+1])
            space[row-1][col+1].g = cal_g(node, space[row-1][col+1])
            space[row-1][col+1].f = space[row-1][col+1].h + space[row-1][col+1].g
            space[row-1][col+1].b = [row, col]
            
        if space[row][col+1] not in opened and space[row][col+1] not in closed and space[row][col+1].h!=1000:
            opened.append(space[row][col+1])
            space[row][col+1].g = cal_g(node, space[row][col+1])
            space[row][col+1].f = space[row][col+1].h + space[row][col+1].g
            space[row][col+1].b = [row, col]
            
        
    elif 0<row and row<lim_row and col==0:
        if space[row-1][col] not in opened and space[row-1][col] not in closed and space[row-1][col].h!=1000:
            opened.append(space[row-1][col])
            space[row-1][col].g = cal_g(node, space[row-1][col])
            space[row-1][col].f = space[row-1][col].h + space[row-1][col].g
            space[row-1][col].b = [row, col]
            
        if space[row-1][col+1] not in opened and space[row-1][col+1] not in closed and space[row-1][col+1].h!=1000:
            opened.append(space[row-1][col+1])
            space[row-1][col+1].g = cal_g(node, space[row-1][col+1])
            space[row-1][col+1].f = space[row-1][col+1].h + space[row-1][col+1].g
            space[row-1][col+1].b = [row, col]
            
        if space[row][col+1] not in opened and space[row][col+1] not in closed and space[row][col+1].h!=1000:
            opened.append(space[row][col+1])
            space[row][col+1].g = cal_g(node, space[row][col+1])
            space[row][col+1].f = space[row][col+1].h + space[row][col+1].g
            space[row][col+1].b = [row, col]
            
        if space[row+1][col+1] not in opened and space[row+1][col+1] not in closed and space[row+1][col+1].h!=1000:
            opened.append(space[row+1][col+1])
            space[row+1][col+1].g = cal_g(node, space[row+1][col+1])
            space[row+1][col+1].f = space[row+1][col+1].h + space[row+1][col+1].g
            space[row+1][col+1].b = [row, col]
            
        if space[row+1][col] not in opened and space[row+1][col] not in closed and space[row+1][col].h!=1000:
            opened.append(space[row+1][col])
            space[row+1][col].g = cal_g(node, space[row+1][col])
            space[row+1][col].f = space[row+1][col].h + space[row+1][col].g
            space[row+1][col].b = [row, col]
                
    return opened

def rewire(node, open_list):
    for i in range(len(open_list)):
        x1 = node.cor[0]
        y1 = node.cor[1]
        x2 = open_list[i].cor[0]
        y2 = open_list[i].cor[1]
        new_g = node.g+math.sqrt((x1-x2)**2 + (y1-y2)**2)
        if new_g < open_list[i].g:
            open_list[i].g = new_g
            open_list[i].f = open_list[i].h + open_list[i].g
            open_list[i].b = [x1, y1]

def pop_from_open(node, open_list, close_list):
    for i in range(len(open_list)):
        if node == open_list[i]:
            poped = open_list.pop(i)
            break
    close_list.append(poped)


obstacles = [[8,1],[8,3],[8,9], [5,1], [0,1], [3,1], [2,2], [3,2], [4,3], [6,2], [6,3], [1,3], [0,5],
             [2,5], [3,5], [6,5], [7,6], [1,7], [3,7], [5,7], [2,8], [3,9], [4,9], [6,8],
             [7,8], [7,9], [6,4], [7,1], [6,1]]
goal=[0,9]
start=[9,0]

rows_dim = 10
cols_dim = 10
space, heuristics = create_space(rows_dim, cols_dim, goal, obstacles)
space[start[0]][start[1]].f = space[start[0]][start[1]].h

close_list = []
close_list.append(space[start[0]][start[1]])

open_list = []
open_list = expand_node(space, space[start[0]][start[1]], open_list, close_list)



while True:
    n_best = find_best(open_list)
    pop_from_open(n_best, open_list, close_list)
    if n_best.cor == goal:
        break
    open_list = expand_node(space, n_best, open_list, close_list)
    rewire(n_best, open_list)
    if len(open_list)==0:
        break


backtracks = []
for i in range (5):
    backtracks.append([])
for i in range(5):
    for j in range(5):
        backtracks[i].append([])
        
for i in range(5):
    for j in range(5):
        backtracks[i][j] = str(space[i][j].b)


x_b = goal[0]
y_b = goal[1]   
back_x = []
back_y = []
back_x.append(y_b+0.5)
back_y.append(rows_dim-1-x_b+0.5)     
while True:
    if [x_b, y_b]==start:
        break
    x_temp = x_b
    y_temp = y_b
    x_b = space[x_temp][y_temp].b[0]
    y_b = space[x_temp][y_temp].b[1]
    back_x.append(y_b+0.5)
    back_y.append(rows_dim-1-x_b+0.5)
    


fig = plt.figure()
ax = fig.gca()
ax.set_xlim([0, rows_dim])
ax.set_ylim([0, cols_dim])
for ob in obstacles:
    x_bot = ob[1]
    y_bot = rows_dim-ob[0]-1
    rect = patches.Rectangle((x_bot,y_bot),1,1,linewidth=1,edgecolor='r',facecolor='r')
    ax.add_patch(rect)
ax.scatter(back_x, back_y)
ax.plot(back_x, back_y)
plt.grid()
plt.show()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
