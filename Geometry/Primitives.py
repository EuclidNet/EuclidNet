import numpy as np
import math
from Utils.utils import *

class Primitive():
    def __init__(self, idx, type, init, goal):
        self.idx = idx
        self.type = type # 0: Point, 1: Line, 2: Circle
        self.goal = goal
        self.init = init

class Point(Primitive):
    def __init__(self, idx, point, init, goal):
        super().__init__(idx, 0, init, goal)
        self.x = point[0]
        self.y = point[1]
        self.loc = point
        
    def __repr__(self):
        rep = 'Point(' + str(self.x) + ',' + str(self.y) + ')'
        return rep

class Line(Primitive):
    def __init__(self, idx, start_point, end_point, init, goal):
        super().__init__(idx, 1, init, goal)
        self.points = []
        self.start_point = start_point
        self.end_point = end_point
        self.m, self.b = two_points_slope_y_intercept(start_point, end_point)
    
    def __repr__(self):
        rep = 'Line: y='+str(self.m)+'x+' + str(self.b) +' from ('+str(self.start_point[0])+','+str(self.start_point[1])+'),('+str(self.end_point[0])+','+str(self.end_point[1])+')'
        return rep

class Circle(Primitive):
    def __init__(self, idx, start_point, end_point, init, goal):
        super().__init__(idx, 2, init, goal)
        self.center = start_point
        self.end_point = end_point
        self.radius = euclid_distance(start_point, end_point)

    def __repr__(self):
        rep = 'Circle: (x-'+ str(self.center[0])+')^2+(y-' + str(self.center[1])+')^2='+str(self.radius)+'^2'
        return rep