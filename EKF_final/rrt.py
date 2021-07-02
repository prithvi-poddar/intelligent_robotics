#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 19:34:52 2021

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy.random import randint as rnd
from numpy.random import uniform as unf
import scipy.stats as stats

class node(object):
    def __init__(self, x, y, b_x, b_y, b_node):
        self.x = x
        self.y = y
        self.b_x = b_x
        self.b_y = b_y
        self.b_node = b_node

class RRT(object):
    def __init__(self, x_lim=100, y_lim=100, start=[5,5], goal=[95,95], num_obs=10, delta = 0.1, distribution='uniform', deviation = None):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.start = start
        self.goal = goal
        self.num_obs = num_obs
        self.generate_obs()
        self.delta = delta
        self.nodes = [node(x=self.start[0], y=self.start[1], b_x=None, b_y=None, b_node=None)]
        self.distribution = distribution
        self.deviation = deviation
        
    def generate_obs(self):
        count = 0
        self.obs_cor = []
        self.obs_rad = []
        while True:
            x = rnd(0, self.x_lim)
            y = rnd(0, self.y_lim)
            rad = rnd(5, 10)
            flag = 0
            
            if (np.hypot((x-self.start[0]), (y-self.start[1]))<(rad+5) or np.hypot((x-self.goal[0]), (y-self.goal[1]))<(rad+5)):
                flag = 1
                
            if (flag == 0):            
                for i in range(len(self.obs_rad)):
                    if (np.hypot((x-self.obs_cor[i][0]), (y-self.obs_cor[i][1])) < rad+self.obs_rad[i]):
                        flag = 1
            if (flag == 1):
                continue
            
            self.obs_cor.append([x,y])
            self.obs_rad.append(rad)
            count += 1
            
            if (count == self.num_obs):
                break
            
    def generate_path(self):
        if (self.distribution == 'uniform'):
            self.generate_path_uniform()
            
        elif (self.distribution == 'biased'):
            self.generate_path_biased()
            
        else:
            self.generate_path_normal()
            
    def generate_path_biased(self):
        print("RRT Biased")
        while True:
            test = np.random.uniform()
            if (test<=0.5):
                qrand = [np.random.uniform(low=0.0, high = self.x_lim),np.random.uniform(low=0.0, high = self.y_lim)]
            else:
                qrand = self.goal
            x = qrand[0]
            y = qrand[1]
            
            distances = []
            for n in self.nodes:
                distances.append(np.hypot((x-n.x), (y-n.y)))
                
            k = np.argmin(distances)
            x1 = self.nodes[k].x
            y1 = self.nodes[k].y
            pt_final = self.get_point([x1,y1], [x,y])
            
            if (self.check_if_in_obs(pt_final) == False):
                self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                # print(pt_final)
                
                if (np.hypot((pt_final[0]-self.goal[0]), (pt_final[1]-self.goal[1])) < 5):
                    break
            
    def generate_path_uniform(self):
        print("RRT uniform distribution")
        while True:
            qrand = [np.random.uniform(low=0.0, high = self.x_lim),np.random.uniform(low=0.0, high = self.y_lim)]
            x = qrand[0]
            y = qrand[1]
            
            distances = []
            for n in self.nodes:
                distances.append(np.hypot((x-n.x), (y-n.y)))
                
            k = np.argmin(distances)
            x1 = self.nodes[k].x
            y1 = self.nodes[k].y
            pt_final = self.get_point([x1,y1], [x,y])
            
            if (self.check_if_in_obs(pt_final) == False):
                self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                # print(pt_final)
                
                if (np.hypot((pt_final[0]-self.goal[0]), (pt_final[1]-self.goal[1])) < 5):
                    break
            
    def generate_path_normal(self):
        print("RRT normal distribution")
        while True:
            lower, upper = 0, self.x_lim
            mu, sigma = self.goal[0], self.deviation
            x = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs(1)[0]
            lower, upper = 0, self.y_lim
            mu, sigma = self.goal[1], self.deviation
            y = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma).rvs(1)[0]
            
            distances = []
            for n in self.nodes:
                distances.append(np.hypot((x-n.x), (y-n.y)))
                
            k = np.argmin(distances)
            x1 = self.nodes[k].x
            y1 = self.nodes[k].y
            pt_final = self.get_point([x1,y1], [x,y])
            
            if (self.check_if_in_obs(pt_final) == False):
                self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                # print(pt_final)
                
                if (np.hypot((pt_final[0]-self.goal[0]), (pt_final[1]-self.goal[1])) < 5):
                    break
            
    def get_point(self, pt1, pt2):
        vec = np.array([(pt2[0]-pt1[0]), (pt2[1]-pt1[1])])
        point = vec/np.linalg.norm(vec)*self.delta
        return point+np.asarray(pt1)
        
    def check_if_in_obs(self, pt):
        x = pt[0]
        y = pt[1]
        
        for i in range(len(self.obs_cor)):
            if(np.hypot((x-self.obs_cor[i][0]), (y-self.obs_cor[i][1])) <= self.obs_rad[i]+1):
                return True
            
        return False
    
    def visualize(self):
        fig = plt.figure(figsize=(15, 10))
        ax = fig.gca()
        ax.set_xlim([0, self.x_lim])
        ax.set_ylim([0, self.y_lim])
        
        for i in range(len(self.obs_cor)):
            x = self.obs_cor[i][0]
            y = self.obs_cor[i][1]
            rad = self.obs_rad[i]
            circle = patches.Circle((x,y),rad,linewidth=1,edgecolor='teal',facecolor='turquoise')
            ax.add_patch(circle)
        for n in self.nodes:
            ax.scatter(n.x, n.y, color='grey', marker='o')
            
        ax.scatter(self.goal[0], self.goal[1], color='black', marker='x')
        ax.scatter(self.start[0], self.start[1], color='black', marker='o')
            
        self.back_x = [self.goal[0]]
        self.back_y = [self.goal[1]]
        n = self.nodes[-1]
        self.back_x.append(n.x)
        self.back_y.append(n.y)
        while True:
            n = n.b_node
            if (n == None):
                break
            self.back_x.append(n.x)
            self.back_y.append(n.y)
        ax.plot(self.back_x, self.back_y, color='black')
        plt.grid(False)
        plt.show()
        
    
