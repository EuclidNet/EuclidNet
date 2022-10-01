from Utils.utils import *
import copy

class SearcherDFS():
    def __init__(self, input_pm, checker, max_depth = 7, max_routine = 200, save = False):
        self.max_depth = max_depth
        self.number_routine = 0
        self.paths = []
        self.pms = []
        self.checker = checker
        for i in range(max_depth+1):
            self.pms.append([])
        self.pms[0].append(input_pm)
        self.sol_found = False
        self.finish_pm = None
        self.sol_path = None
        self.max_routine = max_routine
        self.curr_r = 0
        self.save = save
        
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
        return False

    def line_exist(self, pm, p1, p2):
        for l in pm.lines:
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

    def circle_exist(self, pm , p1, p2):
        for c in pm.circles:
            if p1.x == c.center[0] and p1.y == c.center[1] and p2.x == c.end_point[0] and p2.y == c.end_point[1]:
                return True
            if p1.x == c.center[0] and p1.y == c.center[1] and c.radius == euclid_distance((p1.x,p1.y),(p2.x,p2.y)):
                return True

    def is_used_point(self, used_points, points, interset_pt):
        for up in used_points:
            if up[0] == interset_pt[0] and up[1] == interset_pt[1]:
                return True
        for ep in points:
            if ep.x == interset_pt[0] and ep.y == interset_pt[1]:
                return True
        return False

    def add_intersection(self, pm, verbose = False):
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
        return pm



    def get_pm(self, depth, node):
        return self.pms[depth][node]

    def show_path(self, end_pm):
        path = self.get_path(end_pm)
        for idx, pm in enumerate(path):
            print('Depth:'+str(pm.depth))
            pm.show()
        return path

    def get_path(self, end_pm):
        curr_depth = end_pm.depth
        curr_pm = end_pm
        path = []
        for i in reversed(range(curr_depth + 1)) :
            curr_depth = i
            curr_parent = curr_pm.parent
            path.insert(0,self.pms[curr_depth][curr_pm.node])
            curr_pm = self.pms[curr_depth-1][curr_parent]
        return path

    def next_moves(self, curr_depth, curr_pm, used_line_pairs, used_circle_pairs):
        #reach max depth
        if self.checker.check(curr_pm) and self.sol_found == False:
            self.finish_pm = curr_pm
            curr_pm.finish()
            self.sol_found = True
            self.sol_path = self.get_path(curr_pm)
            return 
        
        if curr_depth == self.max_depth or self.curr_r > self.max_routine or self.sol_found:
            return 


        for p1 in curr_pm.points:
            for p2 in curr_pm.points:
                if p1.x == p2.x and p1.y == p2.y:
                    continue
                if not self.exist_move(used_line_pairs, p1, p2):
                    if not self.line_exist(curr_pm, p1, p2):
                        self.curr_r += 1
                        next_pm = copy.deepcopy(curr_pm)
                        next_pm.update_pm(curr_depth+1, curr_pm.node, len(self.pms[curr_depth+1]))
                        next_pm.create_line( (p1.x,p1.y), (p2.x,p2.y), init = False)
                        next_pm = self.add_intersection(next_pm)
                        used_line_pairs.append( (p1,p2) )
                        self.pms[curr_depth+1].append(next_pm)
                        if self.save:
                            next_pm.save()
                        self.next_moves(curr_depth+1, next_pm, used_line_pairs, used_circle_pairs)
                        used_line_pairs.remove( (p1,p2) )
                if self.sol_found or self.curr_r > self.max_routine:
                    break
                if not self.exist_move_circle(used_circle_pairs, p1, p2):       
                    if not self.circle_exist(curr_pm, p1, p2):
                        self.curr_r += 1
                        next_pm = copy.deepcopy(curr_pm)
                        next_pm.update_pm(curr_depth+1, curr_pm.node, len(self.pms[curr_depth+1]))
                        next_pm.create_circle((p1.x,p1.y), (p2.x,p2.y), init = False)
                        next_pm = self.add_intersection(next_pm)
                        used_circle_pairs.append((p1,p2))
                        self.pms[curr_depth+1].append(next_pm)
                        if self.save:
                            next_pm.save()
                        self.next_moves(curr_depth+1, next_pm, used_line_pairs, used_circle_pairs)
                        used_circle_pairs.remove((p1,p2))

                if self.sol_found or self.curr_r > self.max_routine:
                    break
            if self.sol_found or self.curr_r > self.max_routine:
                    break
                
        