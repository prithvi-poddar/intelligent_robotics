#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 06:42:38 2021

@author: prithvi
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from celluloid import Camera
import time
from rrt_star import *

class Env():
    def __init__(self, x_lim=100, y_lim=100):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.agent = Agent(0, 0, 0)
        
        
    def render(self):
        states = self.agent.state
        print(len(states))
        fig = plt.figure(figsize=(20,20))
        camera = Camera(fig)
        count = 0
        for s in states:
            plt.plot(s[0], s[1], marker=(3, 0, (s[2]*180/np.pi)+30), markersize=20, markerfacecolor='black')
            plt.scatter(self.agent.x_g, self.agent.y_g, marker='x', s=50, color='black')
            plt.xlim([0, self.x_lim])
            plt.ylim([0, self.y_lim])
            camera.snap()
        
        print ('start animation')
        start = time.time()
        animation = camera.animate(blit=False, interval=10)
        animation.save('animation1.mp4')
        print(time.time() - start)
        
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
        print (1)
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
        
            
# =============================================================================
# env = Env()
# env.agent = Agent(5, 5, 90*np.pi/180)
# env.agent.go_to_goal([70,75], 1, 1)
# env.render()
# =============================================================================
            
            
            
            