# import imp
# from turtle import circle
from Geometry.Primitives import Point, Circle, Line
from Utils.Canvas import Canvas
from Utils.utils import *
import shutil
import os

class PrimitivesManager():
    def __init__(self, name, depth = 0, parent = 0, node = 0):
        self.name = name
        self.points = []
        self.circles = []
        self.lines = []
        self.points_goal = []
        self.lines_goal = []
        self.circles_goal = []
        self.curr_idx = 0
        self.sequences = []
        self.intersections = []
        self.parent = 0      
        self.node = node
        self.depth = depth
        img_root_path = './Results/'+str(name)
        self.solution_path = './Results/'+str(name) +'/solution'

        if os.path.exists(img_root_path) == False: 
            os.mkdir(img_root_path)

        img_path = './Results/'+str(name)+'/'+str(depth)
        if os.path.exists(img_path) == False: 
            os.mkdir(img_path)

        filename = str(name)+'_'+str(parent)+'_'+str(node)
        self.cm = Canvas(self.solution_path ,img_path, filename, depth)

        self.isFinsih = False

    def __repr__(self):
        rep = 'D'+str(self.depth) + '#N'+str(self.node) +'#P'+str(self.parent)
        return rep

    def finish(self):
        self.isFinsih = True

    def update_pm(self, depth, parent, node):
        self.depth = depth
        self.parent = parent
        self.node = node
        img_root_path = './Results/'+str(self.name)
        if os.path.exists(img_root_path) == False: 
            os.mkdir(img_root_path)

        img_path = './Results/'+str(self.name)+'/'+str(self.depth)
        if os.path.exists(img_path) == False: 
            os.mkdir(img_path)

        filename = str(self.name)+'_'+str(self.parent)+'_'+str(self.node)
        self.cm.path = img_path
        self.cm.filename = filename

    def get_idx(self):
        self.curr_idx += 1
        return self.curr_idx - 1

    def create_point(self, start_pt, init = False, goal=False):
        new_point = Point(self.get_idx(), start_pt, init, goal)
        self.cm.draw_point(new_point)
        self.sequences.append(new_point)
        if goal:
            self.points_goal.append(new_point)
        else:
            self.points.append(new_point)
        self.remove_duplicated_points()

    def create_line(self, start_pt, end_pt, init = False, goal = False):
        if init:
            new_line = Line(self.get_idx(), start_pt, end_pt, init, goal)
            self.cm.draw_line(new_line)
            if goal:
                self.lines_goal.append(new_line)
            else:
                self.lines.append(new_line)
            self.sequences.append(new_line)
        else:
            new_line = Line(self.get_idx(), start_pt, end_pt, init, goal)
            self.lines.append(new_line)
            self.sequences.append(new_line)
            new_start_pt, new_end_pt = line_project(start_pt, end_pt)
            new_line = Line(self.get_idx(), new_start_pt, new_end_pt, init, goal)
            self.cm.draw_line(new_line)
            self.lines.append(new_line)
            self.sequences.append(new_line)
        self.create_point(start_pt, init, goal)
        self.create_point(end_pt, init, goal)
    
    def create_circle(self, start_pt, end_pt, init = False, goal = False):
        new_circle = Circle(self.get_idx(), start_pt, end_pt, init, goal)
        self.cm.draw_circle(new_circle)
        if goal:
            self.circles_goal.append(new_circle)
        else:
            self.circles.append(new_circle)
        if init == False:
            self.create_point(end_pt, init, goal)
        self.create_point(start_pt, init, goal)


    def remove_duplicated_points(self):
        for idx, pt in enumerate(self.points):
            for idx_2, pt_2 in enumerate(self.points):
                if idx_2 == idx:
                    continue
                if pt.x == pt_2.x and pt.y == pt_2.y:
                    self.points.pop(idx_2)
        for idx, pt in enumerate(self.points_goal):
            for idx_2, pt_2 in enumerate(self.points_goal):
                if idx_2 == idx:
                    continue
                if pt.x == pt_2.x and pt.y == pt_2.y:
                    self.points_goal.pop(idx_2)

    def remove_duplicated_lines(self):
        for idx, line in enumerate(self.lines):
            for idx_2, line_2 in enumerate(self.lines):
                if idx_2 == idx:
                    continue
                if line.m == line_2.m and line.b == line_2.b:
                    self.lines.pop(idx_2)
        for idx, line in enumerate(self.lines_goal):
            for idx_2, line_2 in enumerate(self.lines_goal):
                if idx_2 == idx:
                    continue
                if line.m == line_2.m and line.b == line_2.b:
                    self.lines_goal.pop(idx_2)

    def remove_duplicated_circles(self):
        for idx, line in enumerate(self.circles):
            for idx_2, line_2 in enumerate(self.circles):
                if idx_2 == idx:
                    continue
                if line.m == line_2.m and line.b == line_2.b:
                    self.circles.pop(idx_2)
        for idx, line in enumerate(self.circles_goal):
            for idx_2, line_2 in enumerate(self.circles_goal):
                if idx_2 == idx:
                    continue
                if line.m == line_2.m and line.b == line_2.b:
                    self.circles_goal.pop(idx_2)

    def remove_duplicated_all(self):
        self.remove_duplicated_circles()
        self.remove_duplicated_lines()
        self.remove_duplicated_points()

    def show(self,type=0):
        self.cm.show(type)
    
    def save(self):
        self.cm.save()

    def save_sol(self, depth):
        self.cm.save(depth,True)