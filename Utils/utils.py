from mimetypes import init
import numpy as np
import math
from scipy.spatial import distance
from skspatial import objects

def circle_circle_intersect(circle1, circle2):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    
    x0 = circle1.center[0]
    y0 = circle1.center[1]
    r0 = circle1.radius
    
    x1 = circle2.center[0]
    y1 = circle2.center[1]
    r1 = circle2.radius
    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        if x3 == x4 and y3 == y4:
            return [(x3,y3)]
        else:
            return [(x3, y3), (x4, y4)]

def isBetween(l, p):
    if l.init == False:
        return True
    ax = l.start_point[0]
    ay = l.start_point[1]
    bx = l.end_point[0]
    by = l.end_point[1]
    cxm = p[0]
    cym = p[1]

    x_list = [cxm-1,cxm,cxm+1]
    y_list = [cym-1,cym,cym+1]
    is_false = True
    for cx in x_list:
        for cy in y_list:
            crossproduct = (cy - ay) * (bx - ax) - (cx - ax) * (by - ay)

            # compare versus epsilon for floating point values, or != 0 if using integers

            if abs(crossproduct) > 0.001:
                is_false = False

            dotproduct = (cx - ax) * (bx - ax) + (cy - ay)*(by - ay)
            if dotproduct < 0:
                is_false = False

            squaredlengthba = (bx - ax)*(bx - ax) + (by - ay)*(by - ay)
            if dotproduct > squaredlengthba:
                is_false = False

    return is_false

# def line_circle_intersect(circle, line, full_line=True, tangent_tol=1e-9):
#     """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.
#     :param circle_center: The (x, y) location of the circle center
#     :param circle_radius: The radius of the circle
#     :param pt1: The (x, y) location of the first point of the segment
#     :param pt2: The (x, y) location of the second point of the segment
#     :param full_line: True to find intersections along full line - not just in the segment.  False will just return intersections within the segment.
#     :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
#     :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.
#     """
    
#     circle_center = circle.center
#     circle_radius = circle.radius
#     pt1 = line.start_point 
#     pt2 = line.end_point
#     (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
#     (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
#     dx, dy = (x2 - x1), (y2 - y1)
#     dr = (dx ** 2 + dy ** 2)**.5
#     big_d = x1 * y2 - x2 * y1
#     discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

#     if discriminant < 0:  # No intersection between circle and line
#         return None
#     else:  # There may be 0, 1, or 2 intersections with the segment
#         intersections = [
#             (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
#              cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
#             for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
#         if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
#             fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
#             intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
#         if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
#             return [intersections[0]]
#         else:
#             if len(intersections) == 0:
#                 return None
#             return intersections


def line_circle_intersect(circle, line, full_line=True):
    c = objects.Circle([circle.center[0],circle.center[1]],circle.radius)
    l = objects.Line.from_points([line.start_point[0], line.start_point[1]], [line.end_point[0], line.end_point[1]])
    try:
        p1, p2 = c.intersect_line(l)
    except:
        return None
    if p1[0] == p2[0] and p1[1] == p2[1]:
        if isBetween(line, p1) == True:
            return [(p1[0],p1[1])]
        else:
            return None
    else:
        return_list = []
        if isBetween(line, p1) == True:
            return_list.append((p1[0],p1[1]))
        if isBetween(line, p2) == True:
            return_list.append((p2[0],p2[1]))
        if len(return_list) == 0:
            return None
        else:
            return return_list

def line_line_intersect(line1, line2):
    p1 = line1.start_point 
    p2 = line1.end_point
    p3 = line2.start_point 
    p4 = line2.end_point
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return None
    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return [(x,y)]
        

# def line_line_intersect(line1, line2):
    # l1 = objects.Line.from_points([line1.start_point[0], line1.start_point[1]], [line1.end_point[0], line1.end_point[1]])
    # l2 = objects.Line.from_points([line2.start_point[0], line2.start_point[1]], [line2.end_point[0], line2.end_point[1]])
    # try:
    #     p = l1.intersect_line(l2)
    #     return [(p[0],p[1])]
    # except:
    #     return None

def color(goal = False):
    if goal :
        return (86, 128, 255)
    else:
        return (56, 56, 56)

def thickness(type = 0):# 0: Point, 1: Line, 2: Circle
    if type == 0:
        return -1
    else:
        return 5

def image_size():
    return (512,512)

def slope(start_pt, end_pt):
    if (end_pt[0] - start_pt[0]) == 0: # undefined slope
        m = None
    else:
        m = (end_pt[1] - start_pt[1]) / (end_pt[0] - start_pt[0])
    return m

def line_y_intercept(start_pt, end_pt):
    #y = mx + b
    m = slope(start_pt, end_pt)
    if m != None:
        b = - m * start_pt[0] + start_pt[1]
    else:
        b = None
    return b

def two_points_slope_y_intercept(start_pt, end_pt):
    m = slope(start_pt, end_pt)
    if m != None:
        b = - m * start_pt[0] + start_pt[1]
    else:
        b = None
    return m, b

def point_on_line_xy(start_pt, end_pt, input_x=None, input_y=None):
    b = line_y_intercept(start_pt, end_pt)    
    m = slope(start_pt, end_pt)

    if input_x == None and input_y == None:
        return None

    if m != None:
        if input_x != None:
            y = math.ceil(m*(input_x) + b)
            return (input_x, y)
        else:
            x = math.ceil((input_y-b) / m)
            return (x, input_y)
    elif m == 0:
        if input_x != None:
            y = b
            return (input_x, y)
        else:
            # infinite pts on horizontal line
            return None
    else:
        if input_x != None:
            # infinite pts on vertical line
            return None
        else:
            x = (start_pt[0],input_y)

def euclid_distance(start_pt, end_pt):
    dis = distance.euclidean(start_pt, end_pt)
    dis = math.ceil(dis) 
    return dis

def line_project(start_pt, end_pt):
    m = slope(start_pt,end_pt)
    new_start_pt = start_pt
    new_end_pt = end_pt
    if m == None:
        new_start_pt = (start_pt[0],0)
        new_end_pt = (end_pt[0], image_size()[1])
    elif m == 0:
        new_start_pt = (0,start_pt[1])
        new_end_pt = (image_size()[1], end_pt[1])
    elif m > 0:
        new_start_pt = point_on_line_xy(start_pt, end_pt, input_x=0)
        new_end_pt = point_on_line_xy(start_pt, end_pt, input_x=image_size()[1])
    else: #m<0
        new_start_pt = point_on_line_xy(start_pt, end_pt, input_x=0)
        new_end_pt = point_on_line_xy(start_pt, end_pt, input_x=image_size()[1])
    return new_start_pt, new_end_pt
