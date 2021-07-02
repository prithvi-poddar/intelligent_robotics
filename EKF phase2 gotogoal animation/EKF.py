#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 07:53:10 2021

@author: prithvi
"""
from rrt_star import *
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy.random import randint as rnd
from numpy.random import uniform as unf
import scipy.stats as stats



# =============================================================================
# def generate_obs(n, x_lim, y_lim, start, goal):
#     count = 0
#     obs_cor = []
#     obs_rad = []
#     if (n == 0):
#         return obs_cor, obs_rad
#     while True:
#         x = rnd(0, x_lim)
#         y = rnd(0, y_lim)
#         rad = rnd(5, 10)
#         flag = 0
#         
#         if (np.hypot((x-start[0]), (y-start[1]))<(rad+5) or np.hypot((x-goal[0]), (y-goal[1]))<(rad+5)):
#             flag = 1
#             
#         if (flag == 0):            
#             for i in range(len(obs_rad)):
#                 if (np.hypot((x-obs_cor[i][0]), (y-obs_cor[i][1])) < rad+obs_rad[i]):
#                     flag = 1
#         if (flag == 1):
#             continue
#         
#         obs_cor.append([x,y])
#         obs_rad.append(rad)
#         count += 1
#         
#         if (count == n):
#             break
#         
#     return obs_cor, obs_rad
# 
# def visualize(obs_cor, obs_rad, x_lim, y_lim):
#     fig = plt.figure(figsize=(15, 10))
#     ax = fig.gca()
#     ax.set_xlim([0, x_lim])
#     ax.set_ylim([0, y_lim])
#     
#     for i in range(len(obs_cor)):
#         x = obs_cor[i][0]
#         y = obs_cor[i][1]
#         rad = obs_rad[i]
#         circle = patches.Circle((x,y),rad,linewidth=1,edgecolor='teal',facecolor='turquoise')
#         ax.add_patch(circle)
#     
#     plt.grid(False)
#     plt.show()
#     
# obs_cor, obs_rad = generate_obs(0, 100, 100, [5,5], [90, 90])
# visualize(obs_cor, obs_rad, 100, 100)
# 
# 
# 
# rrt_star = RRT_STAR(x_lim=100, y_lim=100, start=[5,5], goal=[90,90], obs_cor=obs_cor, obs_rad=obs_rad, delta = 0.1, rewire_tolerance=10, distribution='uniform', deviation = None)
# rrt_star.generate_path()
# back_x, back_y = rrt_star.back_track()
# back_x.reverse()
# back_y.reverse()
# rrt_star.visualize()
# 
# path = []
# for i in range(len(back_x)):
#     path.append([back_x[i], back_y[i]])
# 
# 
# 
# =============================================================================
import pickle

with open('path.pkl', 'rb') as f:
    test = pickle.load(f)
from agent import *
env = Env()
env.agent = Agent(5, 5, 90*np.pi/180)
env.agent.follow_path(test)
env.render()





























