from Geometry.Primitives import Circle, Point, Line
import numpy as np
from matplotlib import pyplot as plt
import cv2 
from Utils.utils import *
import os.path

class Canvas():

    def __init__(self, sol_path, path, filename, depth):
        self.img = np.zeros((512,512,3),dtype=np.uint8)
        self.img.fill(255)
        self.sol_path = sol_path
        self.path = path
        self.filename = filename
        self.depth = depth

        self.goal_img = np.zeros((512,512,3),dtype=np.uint8)
        self.goal_img.fill(255)

        self.exist_img = np.zeros((512,512,3),dtype=np.uint8)
        self.exist_img.fill(255)


    def draw_point(self, point):
        if point.goal:
            cv2.circle(self.goal_img, point.loc, 10 , color(point.goal), thickness(point.type))
        else:
            cv2.circle(self.exist_img, point.loc, 10 , color(point.goal), thickness(point.type))
        cv2.circle(self.img, point.loc, 10 , color(point.goal), thickness(point.type))

    def draw_line(self, line):
        if line.goal:
            cv2.line(self.goal_img, line.start_point, line.end_point, color(line.goal), thickness(line.type))
        else:
            cv2.line(self.exist_img, line.start_point, line.end_point, color(line.goal), thickness(line.type))
        cv2.line(self.img, line.start_point, line.end_point, color(line.goal), thickness(line.type))

    def draw_circle(self, circle):
        if circle.goal:
            cv2.circle(self.goal_img, circle.center, circle.radius , color(circle.goal), thickness(circle.type))
        else:
            cv2.circle(self.exist_img, circle.center, circle.radius , color(circle.goal), thickness(circle.type))
        cv2.circle(self.img, circle.center, circle.radius , color(circle.goal), thickness(circle.type))

    def show(self, type = 0): # 0: all, 1: exist 2:goal
        temp = self.img
        if type == 1:
            temp = self.exist_img
        elif type == 2:
            temp = self.goal_img
        plt.imshow(temp)
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def save(self,d ='', sol = False): #ext: _node
        if sol:
            path = os.path.join(self.sol_path +'/'+ str(d) +'.png')
        else:
            path = os.path.join(self.path +'/'+ str(self.filename) +'.png')
        cv2.imwrite(path, cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR))
    
    
