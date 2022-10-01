from Utils.Canvas import Canvas
import numpy as np
import math
from Utils.utils import *
from PIL import Image
from collections import defaultdict

class Checker():

    def __init__(self, pm):
        self.level_0_pm = pm
        im = Image.fromarray(self.level_0_pm.cm.img).convert('RGB')
        by_color = defaultdict(int)
        for pixel in im.getdata():
            by_color[pixel] += 1
        self.orginal_goal = by_color[color(True)]


    def check(self, pm, threshold=2e-1):
        return self.simple_check(pm, threshold)
    
    #check pm by histogram
    def simple_check(self, pm, threshold=2e-1):
        im = Image.fromarray(pm.cm.img).convert('RGB')
        by_color = defaultdict(int)
        for pixel in im.getdata():
            by_color[pixel] += 1
        goal_res = by_color[color(True)]
        if goal_res/self.orginal_goal < threshold :
            return True
        else:
            return False