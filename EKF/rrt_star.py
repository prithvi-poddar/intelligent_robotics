#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 21:36:17 2021

@author: prithvi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy.random import randint as rnd
from numpy.random import uniform as unf
import scipy.stats as stats

class node(object):
    def __init__(self, x, y, b_x, b_y, b_node, cost):
        self.x = x
        self.y = y
        self.b_x = b_x
        self.b_y = b_y
        self.b_node = b_node
        self.cost = cost

class RRT_STAR(object):
    def __init__(self, x_lim=100, y_lim=100, start=[5,5], goal=[90,90], obs_cor=[], obs_rad=[], delta = 0.1, rewire_tolerance=10, distribution='uniform', deviation = None):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.start = start
        self.goal = goal
        self.num_obs = len(obs_cor)
        self.obs_cor = obs_cor
        self.obs_rad = obs_rad
        # self.generate_obs()
        self.delta = delta
        self.nodes = [node(x=self.start[0], y=self.start[1], b_x=None, b_y=None, b_node=None, cost=0)]
        self.rewire_tolerance = rewire_tolerance
        self.distribution = distribution
        self.deviation = deviation
        
# =============================================================================
#     def generate_obs(self):
#         count = 0
#         self.obs_cor = []
#         self.obs_rad = []
#         while True:
#             x = rnd(0, self.x_lim)
#             y = rnd(0, self.y_lim)
#             rad = rnd(5, 10)
#             flag = 0
#             
#             if (np.hypot((x-self.start[0]), (y-self.start[1]))<(rad+5) or np.hypot((x-self.goal[0]), (y-self.goal[1]))<(rad+5)):
#                 flag = 1
#                 
#             if (flag == 0):            
#                 for i in range(len(self.obs_rad)):
#                     if (np.hypot((x-self.obs_cor[i][0]), (y-self.obs_cor[i][1])) < rad+self.obs_rad[i]):
#                         flag = 1
#             if (flag == 1):
#                 continue
#             
#             self.obs_cor.append([x,y])
#             self.obs_rad.append(rad)
#             count += 1
#             
#             if (count == self.num_obs):
#                 break
# =============================================================================
            
    def generate_path(self):
        if (self.distribution == 'uniform'):
            self.generate_path_uniform()
            
        elif (self.distribution == 'biased'):
            self.generate_path_biased()
            
        else:
            self.generate_path_normal()
            
    def generate_path_normal(self):
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
                
                if(self.rewire(pt_final) == False):
                    self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                
                # self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                # print(pt_final)
                
                if (np.hypot((pt_final[0]-self.goal[0]), (pt_final[1]-self.goal[1])) < 5):
                    break
                
            
    def generate_path_biased(self):
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
                
                if(self.rewire(pt_final) == False):
                    self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                
                # self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                # print(pt_final)
                
                if (np.hypot((pt_final[0]-self.goal[0]), (pt_final[1]-self.goal[1])) < 5):
                    break
            
    def generate_path_uniform(self):
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
                
                if(self.rewire(pt_final) == False):
                    self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                
                # self.nodes.append(node(x=pt_final[0], y=pt_final[1], b_x=x1, b_y=y1, b_node=self.nodes[k]))
                # print(pt_final)
                
                if (np.hypot((pt_final[0]-self.goal[0]), (pt_final[1]-self.goal[1])) < 5):
                    break
                
    def rewire(self, pt):
        rewire_nodes = []
        for n in self.nodes:
            if (np.hypot((n.x-pt[0]), (n.y-pt[1])) < self.rewire_tolerance):
                rewire_nodes.append(n)
        costs = []
        for n in rewire_nodes:
            costs.append(n.cost + np.hypot((n.x-pt[0]), (n.y-pt[1])))
            
        found = False
        idx_ = 0
        while (found == False):
            idx = np.argmin(costs)
            n = rewire_nodes[idx]
            if (self.check_line(pt, [n.x, n.y]) == False):
                found = True
                idx_ = idx
            else:
                costs.pop(idx)
                rewire_nodes.pop(idx)
            if (len(costs) == 0):
                break
        if (found == False):
            return False
        else:
            self.nodes.append(node(x=pt[0], y=pt[1], b_x=rewire_nodes[idx_].x, b_y=rewire_nodes[idx_].y, b_node=rewire_nodes[idx_], 
                                   cost=costs[idx_]))
            return True
            
    def check_line(self, pt1, pt2):
        flag = 0
        for i in range(len(self.obs_cor)):
            
            d = np.array([pt2[0]-pt1[0],
                          pt2[1]-pt1[1]])
            f = np.array([pt1[0]-self.obs_cor[i][0],
                          pt1[1]-self.obs_cor[i][1]])
            a = np.dot(d,d)
            b = 2*np.dot(f,d)
            c = np.dot(f,f) - self.obs_rad[i]**2
            
            discriminant = b*b - 4*a*c
            if(discriminant<0):
                continue
            else:
                discriminant = np.sqrt(discriminant)
                t1 = (-b-discriminant)/(2*a)
                t2 = (-b+discriminant)/(2*a)
                
                if(t1>=0 and t1<=1):
                    return True
                if(t2>=0 and t2<=1):
                    return True
                flag=0
                
        return False

    def get_point(self, pt1, pt2):
        vec = np.array([(pt2[0]-pt1[0]), (pt2[1]-pt1[1])])
        point = vec/np.linalg.norm(vec)*self.delta
        return point+np.asarray(pt1)
        
    def check_if_in_obs(self, pt):
        x = pt[0]
        y = pt[1]
        
        for i in range(len(self.obs_cor)):
            if(np.hypot((x-self.obs_cor[i][0]), (y-self.obs_cor[i][1])) <= self.obs_rad[i]+5):
                return True
            
        return False
    
    def back_track(self):
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
        return self.back_x, self.back_y
    
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
        
        
