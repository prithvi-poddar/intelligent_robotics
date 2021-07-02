#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 06:42:38 2021

@author: prithvi
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from celluloid import Camera
import time
from rrt_star import *

class Env():
    def __init__(self, x_lim=100, y_lim=100, obs_cor=[], obs_rad=[]):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.agent = Agent(0, 0, 0)
        self.obs_cor = obs_cor
        self.obs_rad = obs_rad
        
    def render(self):
        states = self.agent.state
        print(len(states))
        fig = plt.figure(figsize=(20,20))
        camera = Camera(fig)
        count = 0
        for s in states:
            print('plotting')
            ax = fig.gca()
            
            plt.xlim([0, self.x_lim])
            plt.ylim([0, self.y_lim])
            
            for i in range(len(self.obs_cor)):
                x = self.obs_cor[i][0]
                y = self.obs_cor[i][1]
                rad = self.obs_rad[i]
                circle = patches.Circle((x,y),rad,linewidth=1,edgecolor='teal',facecolor='turquoise')
                ax.add_patch(circle)
# =============================================================================
#             for n in self.rrt.nodes:
#                 ax.scatter(n.x, n.y, color='grey', marker='o')
# =============================================================================
                
            back__x, back__y = self.rrt.back_track()
                
            ax.scatter(back__x[-1], back__y[-1], color='black', marker='x')
            ax.scatter(back__x[0], back__y[0], color='black', marker='o')
            ax.plot(back__x, back__y, color='black')
            
            plt.plot(s[0], s[1], marker=(3, 0, (s[2]*180/np.pi)+30), markersize=20, markerfacecolor='black')
            plt.scatter(self.agent.x_g, self.agent.y_g, marker='x', s=50, color='black')
            
            camera.snap()
            
        
        print ('start animation')
        start = time.time()
        animation = camera.animate(blit=False, interval=10)
        animation.save('animation1.mp4')
        print(time.time() - start)
        
        
    def generate_path(self, goal=[90, 90]):
        self.rrt = RRT_STAR(x_lim=self.x_lim, y_lim=self.y_lim, start=[self.agent.x,self.agent.y], 
                            goal=goal, obs_cor=self.obs_cor, obs_rad=self.obs_rad, delta = 0.1, rewire_tolerance=10, 
                            distribution='uniform', deviation = None)
        print('Generating path')
        self.rrt.generate_path()
        self.back_x, self.back_y = self.rrt.back_track()
        self.back_x.reverse()
        self.back_y.reverse()
        self.path = []
        for i in range(len(self.back_x)):
            self.path.append([self.back_x[i], self.back_y[i]])
        self.agent.follow_path(self.path)
        self.render()
            

class Agent():
    def __init__(self, x, y, yaw):
        self.x = x
        self.y = y
        self.v = 0
        self.yaw = yaw
        self.ang_speed = 0
        
        self.v_max = 5
        self.ang_speed_max = 0.2 # ~10 degrees/s
        self.dt = 0.1
        
        self.state = [[self.x, self.y, self.yaw]]
        
    def update_pos(self):
        
        self.x = self.x + self.v * np.cos(self.yaw) * self.dt
        self.y = self.y + self.v * np.sin(self.yaw) * self.dt
        self.yaw = self.yaw + self.ang_speed * self.dt
        
    def save_state(self):
        self.state.append([self.x, self.y, self.yaw])
        
        
    def go_to_goal(self, goal, k_linear, k_angular, goal_type):
        print ('Following path')
        self.x_g = goal[0]
        self.y_g = goal[1]
        while True:
            dist = np.hypot((self.x-self.x_g), (self.y-self.y_g))
            self.v = k_linear*dist
            
            desired_angle = math.atan2(self.y_g-self.y, self.x_g-self.x)
            error = desired_angle-self.yaw
            self.ang_speed = error*k_angular
            
            if (self.v > self.v_max):
                self.v = self.v_max
                
            if (self.ang_speed > self.ang_speed_max):
                self.ang_speed = self.ang_speed_max
                
            if (self.ang_speed < -self.ang_speed_max):
                self.ang_speed = -self.ang_speed_max
                
            self.update_pos()
            self.save_state()
            
            if (goal_type == 'final'):
                if (dist < 0.1):
                    break
            else:
                if (dist < 0.3):
                    break
            
    def follow_path(self, path):
        for i in range(len(path)-1):
            self.go_to_goal(path[i], 0.1, 1.5, 'mid')
        self.go_to_goal(path[-1], 0.1, 1.5, 'final')
        
            
env = Env()
env.generate_path()
            
            
            
            