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
#################################################################################        
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
            space[i][j].f = 1000000
            space[i][j].g = 1000000
            
    for obs in obstacles:
        space[obs[0]][obs[1]].h = 100000
    
    heuristics = np.zeros((num_rows,num_cols))
    for i in range(num_rows):
        for j in range(num_cols):
            heuristics[i][j]=space[i][j].h
            
    for i in range(num_rows):
        for j in range(num_cols):
            space[i][j].cor = [i, j]
                            
    return space, heuristics
#################################################################################
def find_best(open_list):
    mini = open_list[0]
    n = len(open_list)
    for i in range(1, n):
        if open_list[i].f<mini.f:
            mini = open_list[i]
    return mini
#################################################################################
def pop_from_open(node, open_list, close_list):
    for i in range(len(open_list)):
        if node == open_list[i]:
            poped = open_list.pop(i)
            break
    close_list.append(poped)
#################################################################################
def expand_node(space, node):
    opened=[]
    lim_row = len(space)-1
    lim_col = len(space[0])-1
    row = node.cor[0]
    col = node.cor[1]
    
    if row<lim_row and col<lim_col and row>0 and col>0:
        if space[row+1][col+1].h != 100000:
            opened.append(space[row+1][col+1])
        if space[row][col+1].h != 100000:
            opened.append(space[row][col+1]) 
        if space[row+1][col].h != 100000:
            opened.append(space[row+1][col])
        if space[row-1][col-1].h != 100000:
            opened.append(space[row-1][col-1])
        if space[row-1][col].h != 100000:
            opened.append(space[row-1][col])
        if space[row][col-1].h != 100000:
            opened.append(space[row][col-1])
        if space[row-1][col+1].h != 100000:
            opened.append(space[row-1][col+1])
        if space[row+1][col-1].h != 100000:
            opened.append(space[row+1][col-1])  
                
    elif row==0 and col==0:
        if space[row+1][col+1].h != 100000:
            opened.append(space[row+1][col+1])
        if space[row][col+1].h != 100000:
            opened.append(space[row][col+1])
        if space[row+1][col].h != 100000:
            opened.append(space[row+1][col])  
        
    elif row==0 and col==lim_col:
        if space[row+1][col].h != 100000:
            opened.append(space[row+1][col])
        if space[row][col-1].h != 100000:
            opened.append(space[row][col-1])
        if space[row+1][col-1].h != 100000:
            opened.append(space[row+1][col-1])
        
    elif row==lim_row and col==0:
        if space[row-1][col].h != 100000:
            opened.append(space[row-1][col])
        if space[row][col+1].h != 100000:
            opened.append(space[row][col+1])
        if space[row-1][col+1].h != 100000:
            opened.append(space[row-1][col+1])
        
    elif row==lim_row and col==lim_col:
        if space[row-1][col-1].h != 100000:
            opened.append(space[row-1][col-1])
        if space[row-1][col].h != 100000:
            opened.append(space[row-1][col])
        if space[row][col-1].h != 100000:
            opened.append(space[row][col-1])
        
    elif row==0 and 0<col and col<lim_col:
        if space[row][col-1].h != 100000:
            opened.append(space[row][col-1])
        if space[row+1][col-1].h != 100000:
            opened.append(space[row+1][col-1])
        if space[row+1][col].h != 100000:
            opened.append(space[row+1][col])
        if space[row+1][col+1].h != 100000:
            opened.append(space[row+1][col+1])
        if space[row][col+1].h != 100000:
            opened.append(space[row][col+1])
        
    elif 0<row and row<lim_row and col==lim_col:
        if space[row-1][col].h != 100000:
            opened.append(space[row-1][col])
        if space[row-1][col-1].h != 100000:
            opened.append(space[row-1][col-1])
        if space[row][col-1].h != 100000:
            opened.append(space[row][col-1])
        if space[row+1][col-1].h != 100000:
            opened.append(space[row+1][col-1])
        if space[row+1][col].h != 100000:
            opened.append(space[row+1][col])
        
    elif row==lim_row and 0<col and col<lim_col:
        if space[row][col-1].h != 100000:
            opened.append(space[row][col-1])
        if space[row-1][col-1].h != 100000:
            opened.append(space[row-1][col-1])
        if space[row-1][col].h != 100000:
            opened.append(space[row-1][col])
        if space[row-1][col+1].h != 100000:
            opened.append(space[row-1][col+1])
        if space[row][col+1].h != 100000:
            opened.append(space[row][col+1])
        
    elif 0<row and row<lim_row and col==0:
        if space[row-1][col].h != 100000:
            opened.append(space[row-1][col])
        if space[row-1][col+1].h != 100000:
            opened.append(space[row-1][col+1])
        if space[row][col+1].h != 100000:
            opened.append(space[row][col+1])
        if space[row+1][col+1].h != 100000:
            opened.append(space[row+1][col+1])
        if space[row+1][col].h != 100000:
            opened.append(space[row+1][col])
        
    return opened
#################################################################################
def dis(current, neighbour):
    x1 = current.cor[0]
    y1 = current.cor[1]
    x2 = neighbour.cor[0]
    y2 = neighbour.cor[1]
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist
#################################################################################
def random_obstacle_generator(lim_row, lim_col, num, goal, start):
    count = 0
    obstacles = []
    while count != num:
        x = np.random.randint(0, lim_row)
        y = np.random.randint(0, lim_col)
        if [x,y] not in obstacles and [x,y]!=goal and [x,y]!=start:
            count += 1
            obstacles.append([x,y])
    return obstacles
#################################################################################
rows_dim = 2000
cols_dim = 2000
goal=[0,1999]
start=[1999,0]
# =============================================================================
# obstacles = random_obstacle_generator(rows_dim, cols_dim, 100, start, goal)
# =============================================================================
# =============================================================================
# obstacles = [[8,1],[8,3],[8,9], [5,1], [0,1], [3,1], [2,2], [3,2], [4,3], [6,2], [6,3], [1,3], [0,5],
#              [2,5], [3,5], [6,5], [7,6], [1,7], [3,7], [5,7], [2,8], [3,9], [4,9], [6,8],
#              [7,8], [7,9], [6,4], [7,1], [6,1], [9,3], [7,3], [2,3],[0,3]]
# =============================================================================
# =============================================================================
# obstacles = [[2,1], [3,1], [1,2], [0,3], [0,4], [1,5], [2,6], [2,7], [2,8], [3,8], [4,8],
#              [5,8], [5,7], [6,6], [6,5], [6,4], [6,3], [5,3], [4,2], [7,6], [7,7], [8,6], [8,7]]
# =============================================================================

obstacles=[]
for i in range(rows_dim):
    for j in range(cols_dim):
        if math.sqrt((i-(rows_dim/2))**2 + (j-(cols_dim/2))**2)<500 and math.sqrt((i-(rows_dim/2))**2 + (j-(cols_dim/2))**2)>450:
            obstacles.append([i,j])

space, heuristics = create_space(rows_dim, cols_dim, goal, obstacles)
space[start[0]][start[1]].g = 0
space[start[0]][start[1]].f = space[start[0]][start[1]].h

open_set = []
close_set = []

open_set.append(space[start[0]][start[1]])
path_found = False

while len(open_set)>0:
    n_best = find_best(open_set)
    if n_best.cor==goal:
        path_found = True
        break
    pop_from_open(n_best, open_set, close_set)
    neighbours = expand_node(space, n_best)
    
    for neighbour in neighbours:
        tentative_g = n_best.g + dis(n_best, neighbour)
        if tentative_g < neighbour.g:
            neighbour.b = n_best.cor
            neighbour.g = tentative_g
            neighbour.f = neighbour.g + neighbour.h
            if neighbour not in open_set:
                open_set.append(neighbour)
     
if path_found:
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
    #ax.scatter(back_x, back_y)
    ax.plot(back_x, back_y)
    plt.grid()
    plt.show()


#### to plot explored points #####
# =============================================================================
# x_ex=[]
# y_ex=[]
# for n in close_set:
#     x_ex.append(n.cor[1]+0.5)
#     y_ex.append(rows_dim-1-n.cor[0]+0.5)
# fig = plt.figure()
# ax = fig.gca()
# ax.set_xlim([0, rows_dim])
# ax.set_ylim([0, cols_dim])
# for ob in obstacles:
#     x_bot = ob[1]
#     y_bot = rows_dim-ob[0]-1
#     rect = patches.Rectangle((x_bot,y_bot),1,1,linewidth=1,edgecolor='r',facecolor='r')
#     ax.add_patch(rect)
# ax.scatter(x_ex,y_ex)
# plt.grid()
# plt.show()
# =============================================================================

    























