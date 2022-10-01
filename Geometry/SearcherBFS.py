from hashlib import new
from matplotlib.pyplot import gray
from matplotlib import pyplot as plt
from matplotlib.style import use
from Geometry.PrimitivesManager import PrimitivesManager
from Utils.utils import *
import copy
import numpy as np
import cv2

class SearcherBFS():
    def __init__(self, pm, depth, parent):
        self.used_line_pairs = [] # (p1,p2)
        self.used_circle_pairs = []
        self.used_point = []
        self.last_pm = pm
        self.new_pms = []
        self.depth = depth
        self.name = self.last_pm.name
        self.node = 0
        self.parent = parent

    def get_node(self):
        self.node += 1
        return self.node - 1
    def exist_move(self, used_pairs, p1, p2):
        for pair in used_pairs:
            up1 = pair[0]
            up2 = pair[1]
            if p1.x==up1.x and p1.y==up1.y and p2.x==up2.x and p2.y==up2.y:
                return True
            if p2.x==up1.x and p2.y==up1.y and p1.x==up2.x and p1.y==up2.y:
                return True
        return False

    def exist_move_circle(self, used_pairs, p1, p2):
        for pair in used_pairs:
            up1 = pair[0]
            up2 = pair[1]
            if p1.x==up1.x and p1.y==up1.y and p2.x==up2.x and p2.y==up2.y:
                return True
            if p1.x==up1.x and p1.y==up1.y and euclid_distance((up1.x,up1.y),(up2.x,up2.y)) == euclid_distance((p1.x,p1.y),(p2.x,p2.y)):
                return True
            # if p2.x==up1.x and p2.y==up1.y and p1.x==up2.x and p1.y==up2.y:
            #     return True
        return False

    #E1: draw unique straight line
    def create_possible_line(self, input_pm, p1, p2, verbose = False):
        for l in input_pm.lines:
            if p1.x == l.start_point[0] and p1.y == l.start_point[1] and p2.x == l.end_point[0] and p2.y == l.end_point[1]:
                return True
            if p2.x == l.start_point[0] and p2.y == l.start_point[1] and p1.x == l.end_point[0] and p1.y == l.end_point[1]:
                return True
            # same slope
            if slope((p1.x,p1.y),(p2.x,p2.y)) == None and l.m == None:
                if p1.x == l.start_point[0]:
                    return True
            elif slope((p1.x,p1.y),(p2.x,p2.y)) == l.m:
                return True

        new_pm = copy.deepcopy(input_pm)
        new_pm.update_pm(self.depth, self.parent, self.get_node())
        new_pm.create_line( (p1.x,p1.y),
                            (p2.x,p2.y), 
                            init = False)
        if verbose:
            print('Line', (p1.x,p1.y),(p2.x,p2.y))
            new_pm.show()
            # new_pm.save()
        self.used_line_pairs.append( (p1,p2) )
        return new_pm

    #E2: draw circle from center
    def create_possible_circle(self, input_pm, p1, p2, verbose = False):
        for c in input_pm.circles:
            if p1.x == c.center[0] and p1.y == c.center[1] and p2.x == c.end_point[0] and p2.y == c.end_point[1]:
                return True
            if p1.x == c.center[0] and p1.y == c.center[1] and c.radius == euclid_distance((p1.x,p1.y),(p2.x,p2.y)):
                return True
        new_pm = copy.deepcopy(input_pm)
        new_pm.update_pm(self.depth, self.parent, self.get_node())
        new_pm.create_circle((p1.x,p1.y),
                             (p2.x,p2.y),
                             init = False)
        
        if verbose:
            print('Circle',(p1.x,p1.y),(p2.x,p2.y))
            new_pm.show()
            # new_pm.save()
        self.used_circle_pairs.append( (p1,p2) )
        return new_pm

    def search_possible_moves(self, verbose = False):
        self.new_pms = []

        for p1 in self.last_pm.points:
            for p2 in self.last_pm.points:
                if p1.x == p2.x and p1.y == p2.y:
                    continue
                if not self.exist_move(self.used_line_pairs, p1,p2):
                    new_move = self.create_possible_line(self.last_pm, p1, p2, verbose)
                    if new_move != True:
                        self.new_pms.append(new_move)

        for p1 in self.last_pm.points:
            for p2 in self.last_pm.points:
                if p1.x == p2.x and p1.y == p2.y:
                    continue
                if not self.exist_move_circle(self.used_circle_pairs, p1,p2):
                    new_move = self.create_possible_circle(self.last_pm,p1,p2, verbose)
                    if new_move != True:
                        self.new_pms.append(new_move)
        return self.new_pms

    def is_used_point(self, used_points, points, interset_pt):
        for up in used_points:
            if up[0] == interset_pt[0] and up[1] == interset_pt[1]:
                return True
        for ep in points:
            if ep.x == interset_pt[0] and ep.y == interset_pt[1]:
                return True
        return False

    def search_possible_intersection(self, idx_d, verbose = False):
        d = self.depth
        for idx, pm in enumerate(self.new_pms):
            used_points = []
            lines = pm.lines
            circles = pm.circles
            points = pm.points

            # line-line
            for l1 in lines:
                for l2 in lines:
                    if l1 is not l2:
                        res = line_line_intersect(l1, l2)
                        if res != None:
                            interset_pt = res[0]
                            interset_pt = [round(x) for x in interset_pt]
                            #check used pt on new/old set
                            if self.is_used_point(used_points, points, interset_pt) == False:
                                pm.create_point(interset_pt, init = False)
                                used_points.append(interset_pt)
            #line-circle
            for c in circles:
                for l in lines:
                    if c is not l:
                        res = line_circle_intersect(c,l,l.init)
                        if res != None:
                            if len(res) == 1:
                                interset_pt = res[0]
                                interset_pt = [round(x) for x in interset_pt]
                                if self.is_used_point(used_points, points, interset_pt) == False:
                                    pm.create_point(interset_pt, init = False)
                                    used_points.append(interset_pt)
                            else:
                                interset_pt1 = res[0]
                                interset_pt1 = [round(x) for x in interset_pt1]
                                if self.is_used_point(used_points, points, interset_pt1) == False:
                                    pm.create_point(interset_pt1, init = False)
                                    used_points.append(interset_pt1)
                                interset_pt2 = res[1]
                                interset_pt2 = [round(x) for x in interset_pt2]
                                if self.is_used_point(used_points, points, interset_pt2) == False:
                                    pm.create_point(interset_pt2, init = False)
                                    used_points.append(interset_pt2)
            #circle-circle
            for c1 in circles:
                for c2 in circles:
                    if c1 is not c2:
                        res = circle_circle_intersect(c1,c2)
                        if res != None:
                            if len(res) == 1:
                                interset_pt = res[0]
                                interset_pt = [round(x) for x in interset_pt]
                                if self.is_used_point(used_points, points, interset_pt) == False:
                                    pm.create_point(interset_pt, init = False)
                                    used_points.append(interset_pt)
                            else:
                                interset_pt1 = res[0]
                                interset_pt1 = [round(x) for x in interset_pt1]
                                if self.is_used_point(used_points, points, interset_pt1) == False:
                                    pm.create_point(interset_pt1, init = False)
                                    used_points.append(interset_pt1)
                                interset_pt2 = res[1]
                                interset_pt2 = [round(x) for x in interset_pt2]
                                if self.is_used_point(used_points, points, interset_pt2) == False:
                                    pm.create_point(interset_pt2, init = False)
                                    used_points.append(interset_pt2)

            if verbose:
                pm.show()
        return self.new_pms