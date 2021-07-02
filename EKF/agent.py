#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 06:42:38 2021

@author: prithvi
"""

import numpy as np
from numpy.random import randint as rnd
from numpy.random import uniform as unf
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from celluloid import Camera
import time
from rrt_star import *
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--gps_time", default="1", type=int, required=True)
args = parser.parse_args()



def generate_obs(n, x_lim, y_lim, start, goal):
    count = 0
    obs_cor = []
    obs_rad = []
    if (n == 0):
        return obs_cor, obs_rad
    while True:
        x = rnd(0, x_lim)
        y = rnd(0, y_lim)
        rad = rnd(5, 10)
        flag = 0
        
        if (np.hypot((x-start[0]), (y-start[1]))<(rad+5) or np.hypot((x-goal[0]), (y-goal[1]))<(rad+5)):
            flag = 1
            
        if (flag == 0):            
            for i in range(len(obs_rad)):
                if (np.hypot((x-obs_cor[i][0]), (y-obs_cor[i][1])) < rad+obs_rad[i]):
                    flag = 1
        if (flag == 1):
            continue
        
        obs_cor.append([x,y])
        obs_rad.append(rad)
        count += 1
        
        if (count == n):
            break
        
    return obs_cor, obs_rad

def visualize(obs_cor, obs_rad, x_lim, y_lim):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.gca()
    ax.set_xlim([0, x_lim])
    ax.set_ylim([0, y_lim])
    
    for i in range(len(obs_cor)):
        x = obs_cor[i][0]
        y = obs_cor[i][1]
        rad = obs_rad[i]
        circle = patches.Circle((x,y),rad,linewidth=1,edgecolor='teal',facecolor='turquoise')
        ax.add_patch(circle)
    
    plt.grid(False)
    plt.show()
    
# =============================================================================
# obs_cor, obs_rad = generate_obs(10, 100, 100, [5,5], [90, 90])
# visualize(obs_cor, obs_rad, 100, 100)
# =============================================================================
with open('obs_cor.pkl', 'rb') as f:
    obs_cor = pickle.load(f)
    
with open('obs_rad.pkl', 'rb') as f:
    obs_rad = pickle.load(f)
    


class Env():
    def __init__(self, x_lim=100, y_lim=100, obs_cor=[], obs_rad=[], gps_time=args.gps_time): #args.gps_time
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.gps_time = gps_time
        self.obs_cor = obs_cor
        self.obs_rad = obs_rad
        self.agent = Agent(0, 0, 0, self.gps_time, self.obs_cor, self.obs_rad)
        
        
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
#             if (count <= 50):
#                 
#                 for n in self.rrt.nodes:
#                     ax.scatter(n.x, n.y, color='grey', marker='o')
# =============================================================================
                
            back__x, back__y = self.rrt.back_track()
                
            ax.scatter(back__x[-1], back__y[-1], color='black', marker='x')
            ax.scatter(back__x[0], back__y[0], color='black', marker='o')
            ax.plot(back__x, back__y, color='black')
            
            plt.plot(s[0], s[1], marker=(3, 1, (s[2]*180/np.pi)+30), markersize=20, markerfacecolor='black', markeredgecolor='black')
            plt.plot(s[3], s[4], marker=(3, 1, (s[5]*180/np.pi)+30), markersize=20, markerfacecolor='lightcoral', markeredgecolor='lightcoral')
            u=s[3]               #x-position of the center
            v=s[4]               #y-position of the center
            a=s[6].item(0,0)     #radius on the x-axis
            b=s[6].item(1,1)     #radius on the y-axis
            
            t = np.linspace(0, 2*np.pi, 100)
            plt.plot( u+a*np.cos(t) , v+b*np.sin(t), color='black')
            plt.scatter(self.agent.x_g, self.agent.y_g, marker='x', s=50, color='black')
            
            camera.snap()            
            count += 1
            
        
        print ('start animation')
        start = time.time()
        animation = camera.animate(blit=False, interval=100) #blit=False, interval=10
        animation.save('animation_test_%ssec.mp4'%str(self.gps_time))
        print(time.time() - start)
        
        
    def generate_path(self, goal=[90, 90]):
        with open('rrt_instance.pkl', 'rb') as f:
            self.rrt = pickle.load(f)
        print ('rrt loaded')
        
# =============================================================================
#         self.rrt = RRT_STAR(x_lim=self.x_lim, y_lim=self.y_lim, start=[self.agent.x,self.agent.y], 
#                             goal=goal, obs_cor=self.obs_cor, obs_rad=self.obs_rad, delta = 0.1, rewire_tolerance=10, 
#                             distribution='uniform', deviation = None)
#         print('Generating path')
#         self.rrt.generate_path()
# =============================================================================
        self.back_x, self.back_y = self.rrt.back_track()
        self.back_x.reverse()
        self.back_y.reverse()
        self.path = []
        for i in range(len(self.back_x)):
            self.path.append([self.back_x[i], self.back_y[i]])
# =============================================================================
#         with open('path.pkl', 'rb') as f:
#             self.path = pickle.load(f)
# =============================================================================
        self.agent.follow_path(self.path)
        self.render()
            

class Agent():
    def __init__(self, x, y, yaw, gps_time, obs_cor, obs_rad):
        self.x = x
        self.y = y
        self.v = 0
        self.yaw = yaw
        self.ang_speed = 0
        self.gps_time = gps_time
        self.obs_cor = obs_cor
        self.obs_rad = obs_rad
        
        self.x_bel = self.x
        self.y_bel = self.y
        self.yaw_bel = self.yaw
        self.error_cov = np.matrix([[0.001, 0, 0],
                                   [0, 0.001, 0],
                                   [0, 0, 0.005]])
        
        self.motion_cov = np.matrix([[1.5, 0, 0],
                                    [0, 1.5, 0],
                                    [0, 0, 0.01]])
        self.Q_t = np.matrix([[0.001, 0],
                             [0, 0.001]])
        
        self.v_max = 5
        self.ang_speed_max = 0.7 # ~45 degrees/s
        self.dt = 0.1
        self.time_elapsed = 0
        
        self.state = [[self.x, self.y, self.yaw, self.x_bel, self.y_bel, self.yaw_bel, self.motion_cov]]
        
    def update_pos(self):
        error = np.random.multivariate_normal(np.zeros(3), self.error_cov)
        self.x = self.x + self.v * np.cos(self.yaw) * self.dt + (error[0])
        self.y = self.y + self.v * np.sin(self.yaw) * self.dt + (error[1])
        self.yaw = self.yaw + self.ang_speed * self.dt + error[2]
        self.ekf(self.v, self.ang_speed)
        self.time_elapsed += self.dt
        
        if (round(self.time_elapsed, 1) % self.gps_time == 0):
            self.x_bel = self.x
            self.y_bel = self.y
            self.yaw_bel = self.yaw
            self.motion_cov = np.matrix([[1, 0, 0],
                                        [0, 1, 0],
                                        [0, 0, 0.01]])
            
    def get_obs_cor(self):
        if (len(self.obs_cor) == 0):
            return None
        else:
            got = 0
            min_dist = 1000
            for i in range(len(self.obs_cor)):
                if (np.hypot((self.x - self.obs_cor[i][0]), (self.y - self.obs_cor[i][1])) <= self.obs_rad[i] + 5):
                    got = 1
                    min_obs = self.obs_cor[i]
                    if (np.hypot((self.x - self.obs_cor[i][0]), (self.y - self.obs_cor[i][1])) - self.obs_rad[i] < min_dist):
                        min_dist = np.hypot((self.x - self.obs_cor[i][0]), (self.y - self.obs_cor[i][1])) - self.obs_rad[i]
                        min_obs = self.obs_cor[i]
            if(got == 0):
                return None
            else:
                return min_obs
            
    def actual_obs(self, obs):
        xg = obs[0]
        yg = obs[1]
        X_ = (xg-self.x)*np.cos(self.yaw) + (yg-self.y)*np.sin(self.yaw)
        Y_ = (yg-self.y)*np.cos(self.yaw) - (xg-self.x)*np.sin(self.yaw)
        return X_, Y_
                
        
    def ekf(self, v, w):
        self.G = np.matrix([[1, 0, -self.v * np.cos(self.yaw_bel) * self.dt],
                            [0, 1, self.v * np.sin(self.yaw_bel) * self.dt ],
                            [0, 0,                1                        ]])
        self.x_bel = self.x_bel + self.v * np.cos(self.yaw_bel) * self.dt
        self.y_bel = self.y_bel + self.v * np.sin(self.yaw_bel) * self.dt
        self.yaw_bel = self.yaw_bel + self.ang_speed * self.dt
        self.mu = np.matrix([[self.x_bel],
                             [self.y_bel],
                             [self.yaw_bel]])
        self.motion_cov = self.G @ self.motion_cov @ self.G.T + self.error_cov
        
        min_obs = self.get_obs_cor()
        if (min_obs == None):
            pass
        else:
            X_, Y_ = self.actual_obs(min_obs)
            z_t = np.matrix([[X_],
                             [Y_]])
            H = np.matrix([[-np.cos(self.yaw_bel), -np.sin(self.yaw_bel), (self.x_bel-X_)*np.sin(self.yaw_bel) + (Y_-self.y_bel)*np.cos(self.yaw_bel)],
                          [np.sin(self.yaw_bel),  -np.cos(self.yaw_bel), (self.x_bel-X_)*np.cos(self.yaw_bel) + (self.y_bel-Y_)*np.sin(self.yaw_bel)]])
            h = np.matrix([[(X_-self.x_bel)*np.cos(self.yaw_bel) + (Y_-self.y_bel)*np.sin(self.yaw_bel)],
                           [(Y_-self.y_bel)*np.cos(self.yaw_bel) - (X_-self.x_bel)*np.sin(self.yaw_bel)]])
            
            k_t = self.motion_cov @ H.T @ np.linalg.pinv(H @ self.motion_cov @ H.T + self.Q_t)
            
            self.mu = self.mu + k_t @ (z_t - h)
            self.motion_cov = (np.eye(np.matmul(k_t, H).shape[0]) - np.matmul(k_t, H)) @ self.motion_cov
        
        
        
    def save_state(self):
        self.state.append([self.x, self.y, self.yaw, self.x_bel, self.y_bel, self.yaw_bel, self.motion_cov])
        
        
    def go_to_goal(self, goal, k_linear, k_angular, goal_type, next_point):
        print ('Following path')
        self.x_g = goal[0]
        self.y_g = goal[1]
        while True:
            dist = np.hypot((self.x_bel-self.x_g), (self.y_bel-self.y_g))
            self.v = k_linear*dist
            
            desired_angle = math.atan2(self.y_g-self.y_bel, self.x_g-self.x_bel)
            error = desired_angle-self.yaw_bel
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
                if (dist < 1):
                    break
                
                vector_1 = np.array([self.x_g - self.x_bel, self.y_g - self.y_bel])
                vector_2 = np.array([next_point[0] - self.x_bel, next_point[1] - self.y_bel])
                
                unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
                unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
                dot_product = np.dot(unit_vector_1, unit_vector_2)
                angle = np.arccos(dot_product)*180/np.pi
                if (angle > 90):
                    break
            
    def follow_path(self, path):
        for i in range(1, len(path)-1):
            self.go_to_goal(path[i], 0.5, 1.5, 'mid', path[i+1])
        self.go_to_goal(path[-1], 0.5, 1.5, 'final', [])
        
            
env = Env(obs_cor=obs_cor, obs_rad=obs_rad)
env.generate_path()

