import imp
from Geometry.SearcherBFS import SearcherBFS
from Geometry.SearcherDFS import SearcherDFS
from Geometry.PrimitivesManager import PrimitivesManager
from Utils.Checker import Checker
import os
import enum
import sys
import random
import math
import numpy as np
from pdb import pm
import math
from os import walk, getcwd
random.seed(2022)
ROOT_DIR = os.path.abspath("./")
sys.path.append(ROOT_DIR) 
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log
from mrcnn.visualize import display_instances
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import warnings
warnings.filterwarnings("ignore")

MAX_DEPTH = 6
MODEL_DIR = os.path.join('./Data/Models/', "logs")
MODEL_P_PATH = './Data/Models/Primitives.h5'
MODEL_I_PATH = './Data/Models/Intersection.h5'
CLASSES_P = ['Point','Line','Circle']
CLASSES_I = ['LL','LC','CC']
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)
class EuclidNetConfig(Config):
    NAME = "EuclidNet"
    BACKBONE = "resnet101"
    NUM_CLASSES = 1 + 3
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2
class InferenceConfig(EuclidNetConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2
    DETECTION_MIN_CONFIDENCE = 0.997
inference_config = InferenceConfig()

class SearchManager():
    def __init__(self, input_pm,m_i, m_p, max_depth = 7, max_routine=100000):
        self.searchers = [] # for each depth
        self.max_depth = max_depth
        self.current_depth = 0
        self.level_0_pm = input_pm
        self.next_possible_moves = [] # list of PM
        self.m_i = m_i
        self.m_p = m_p
        self.checker = Checker(self.level_0_pm)
        self.finsih_pm = None
        self.sol_found = False
        self.sol_path = None

        self.max_routine = max_routine

    def start(self, s = 'DFS', verbose=False):
        if s == 'BFS':
            self.start_BFS(verbose)
        else:
            self.start_DFS(verbose)


    def solution(self):
        if self.sol_found:
            if os.path.exists(self.finsih_pm.solution_path) == False: 
                os.mkdir(self.finsih_pm.solution_path)

            for idx, pm in enumerate(self.sol_path):
                print('Depth:'+str(pm.depth))
                pm.show()
                pm.save_sol(pm.depth)

        else:
            print('Solution Not Found.')

    def start_DFS(self, verbose=False):
        
        input_pm = self.level_0_pm

        sh = SearcherDFS(input_pm, self.checker, self.max_depth, self.max_routine, verbose)

        sh.next_moves(0,input_pm,[],[])
        if sh.sol_found:
            sh.show_path(sh.finish_pm)
            self.finsih_pm = sh.finish_pm
            self.sol_found = True
            self.sol_path = sh.sol_path


    def start_BFS(self, verbose=False):
        print('Depth:',0)
        input_pm = self.level_0_pm
        self.next_possible_moves = [input_pm]
        for idx, curr_depth in enumerate(range(1, self.max_depth+1)):
            print('Depth:',curr_depth)
            sl = []
            for idx_d, moves in enumerate(self.next_possible_moves):
                sh = SearcherBFS(  moves, 
                                depth = curr_depth, 
                                parent = moves.node)

                self.next_possible_moves = sh.search_possible_moves(False)
                self.next_possible_moves = sh.search_possible_intersection(idx_d, False)
                print('New moves:', len(self.next_possible_moves))

                for idx_t, pm in enumerate(self.next_possible_moves):
                    # print(idx_t)
                    pm.save()
                    if verbose:
                        pm.show()
                    if self.checker.check(pm):
                        print('Problem solved!')
                        pm.finsih()
                        self.finsih_pm = pm
                        self.sol_found = True
                        pm.show()
                sl.append(sh)
            self.searchers.append(sl)