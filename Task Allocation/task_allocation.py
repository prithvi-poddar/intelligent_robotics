#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:39:19 2020

@author: prithvi
"""

from __future__ import print_function
from ortools.linear_solver import pywraplp
import numpy as np
import math

class agent():
    def __init__(self, name=0, cor=[0,0]):
        self.name = name
        self.cor = cor

class task():
    def __init__(self, name=0, cor=[0,0]):
        self.name = name
        self.cor = cor

def spawn(sapce, n_agents, n_tasks):
    x_lim = space[0]
    y_lim = space[1]
    
    tasks=[]
    for i in range(n_tasks):
        tasks.append([])
    for i in range(n_tasks):
        tasks[i]=task()
    
    agents = []
    for i in range(n_agents):
        agents.append([])
    for i in range(n_agents):
        agents[i]=agent()        
    
    count = 1
    occupied = []
    while count<=n_tasks:
        [x,y] = [np.random.randint(0, x_lim), np.random.randint(0, y_lim)]
        if [x,y] not in occupied:
            occupied.append([x,y])
            tasks[count-1].name = count
            tasks[count-1].cor = [x,y]
            count = count+1            
            
    count = 1
    while count<=n_agents:
        [x,y] = [np.random.randint(0, x_lim), np.random.randint(0, y_lim)]
        if [x,y] not in occupied:
            occupied.append([x,y])
            agents[count-1].name = count
            agents[count-1].cor = [x,y]
            count = count+1      
        
    return tasks, agents   

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def get_cost(tasks, agents):
    cost = []
    for i in range(len(agents)):
        cost.append([])
    for i in range(len(agents)):
        for j in range(len(tasks)):
            cost[i].append([])
            
    for i in range(len(agents)):
        for j in range(len(tasks)):
            cost[i][j] = dist(agents[i].cor[0], agents[i].cor[1], tasks[j].cor[0], tasks[j].cor[1])
            
    return cost
    
n_agents = 10
n_tasks = 10
space = [100,100]
x={}

tasks, agents = spawn(space, n_agents, n_tasks)
cost = get_cost(tasks, agents)

solver = pywraplp.Solver('SolveAssignmentProblemMIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

for i in range(n_agents):
    for j in range(n_tasks):
        x[i,j] = solver.BoolVar('x[%i,%i' % (i,j))
        
solver.Minimize(solver.Sum([cost[i][j] * x[i,j] for i in range(n_agents)
                                                for j in range(n_tasks)]))
# constraints
# Each worker is assigned to at least 1 task.

for i in range(n_agents):
    solver.Add(solver.Sum([x[i, j] for j in range(n_tasks)]) >= 1)
    
# Each task is assigned to exactly one worker.
for j in range(n_tasks):
    if (j == 4):
        solver.Add(solver.Sum([x[i, j] for i in range(n_agents)]) == 5)
    else:
        solver.Add(solver.Sum([x[i, j] for i in range(n_agents)]) == 1)
    
sol = solver.Solve()

print('Total cost = ', solver.Objective().Value())
print()
for i in range(n_agents):
    for j in range(n_tasks):
        if x[i, j].solution_value() > 0:
            print('Worker %d assigned to task %d.  Cost = %d' % (i, j, cost[i][j]))
            
print()
print("Time = ", solver.WallTime(), " milliseconds")


