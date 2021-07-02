#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 15:00:45 2021

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt

class Cell():
    def __init__(self, h=-1, k=-1, cor=[0,0], back=[-1,-1]):
        self.h = h
        self.k = k
        self.cor = cor
        self.back = back
        
def create_space(num_rows, num_cols, obstacles=[]):
    space = []
    for i in range (num_rows):
        space.append([])
    for i in range(num_rows):
        for j in range(num_cols):
            space[i].append([])
            
    for i in range(num_rows):
        for j in range(num_cols):
            space[i][j] = Cell(cor=[i,j])
            
    for obs in obstacles:
        space[obs[0]][obs[1]].h = float('inf')
                            
    return space

def find_best(open_list):
    mini = open_list[0]
    n = len(open_list)
    for i in range(1, n):
        if open_list[i].f<mini.f:
            mini = open_list[i]
    return mini

def pop_from_open(node, open_list, close_list):
    for i in range(len(open_list)):
        if node == open_list[i]:
            poped = open_list.pop(i)
            break
    close_list.append(poped)

def expand_node(space, node):
    opened=[]
    lim_row = len(space)-1
    lim_col = len(space[0])-1
    row = node.cor[0]
    col = node.cor[1]
    
    if row<lim_row and col<lim_col and row>0 and col>0:
        opened.append(space[row+1][col+1])
        opened.append(space[row][col+1]) 
        opened.append(space[row+1][col])
        opened.append(space[row-1][col-1])
        opened.append(space[row-1][col])
        opened.append(space[row][col-1])
        opened.append(space[row-1][col+1])
        opened.append(space[row+1][col-1])  
                
    elif row==0 and col==0:
        opened.append(space[row+1][col+1])
        opened.append(space[row][col+1])
        opened.append(space[row+1][col])  
        
    elif row==0 and col==lim_col:
        opened.append(space[row+1][col])
        opened.append(space[row][col-1])
        opened.append(space[row+1][col-1])
        
    elif row==lim_row and col==0:
        opened.append(space[row-1][col])
        opened.append(space[row][col+1])
        opened.append(space[row-1][col+1])
        
    elif row==lim_row and col==lim_col:
        opened.append(space[row-1][col-1])
        opened.append(space[row-1][col])
        opened.append(space[row][col-1])
        
    elif row==0 and 0<col and col<lim_col:
        opened.append(space[row][col-1])
        opened.append(space[row+1][col-1])
        opened.append(space[row+1][col])
        opened.append(space[row+1][col+1])
        opened.append(space[row][col+1])
        
    elif 0<row and row<lim_row and col==lim_col:
        opened.append(space[row-1][col])
        opened.append(space[row-1][col-1])
        opened.append(space[row][col-1])
        opened.append(space[row+1][col-1])
        opened.append(space[row+1][col])
        
    elif row==lim_row and 0<col and col<lim_col:
        opened.append(space[row][col-1])
        opened.append(space[row-1][col-1])
        opened.append(space[row-1][col])
        opened.append(space[row-1][col+1])
        opened.append(space[row][col+1])
        
    elif 0<row and row<lim_row and col==0:
        opened.append(space[row-1][col])
        opened.append(space[row-1][col+1])
        opened.append(space[row][col+1])
        opened.append(space[row+1][col+1])
        opened.append(space[row+1][col])
        
    return opened

def dis(current, neighbour):
    x1 = current.cor[0]
    y1 = current.cor[1]
    x2 = neighbour.cor[0]
    y2 = neighbour.cor[1]
    dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist







