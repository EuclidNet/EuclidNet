from Geometry.PrimitivesManager import PrimitivesManager
from Geometry.SearchManagerNew import SearchManager

import enum
import os
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
import argparse
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

def create_init_pm(img, model_p, model_i):
    p_results = model_p.detect([img], verbose=0)
    r = p_results[0]
    pm = PrimitivesManager('CircleThroughPoint')
    for idx, val in enumerate(len(r['rois'])):
        # cls = CLASSES_P[r['class_ids']]
        xmin , ymin, xmax, ymax =  r['rois'][idx]
        if r['class_ids'][idx] == 0: #Point
            pm.create_point(((xmin+xmax)/2, (ymin+ymax)/2), init = True)
        elif r['class_ids'][idx] == 1: #Line
            pm.create_line( (xmin,ymin),(xmax,ymax), init = True)
        else: #circle
            pm.create_circle(((xmin+xmax)/2, (ymin+ymax)/2),((xmin+xmax)/2,ymin), init = True, goal=True)
    return pm

def search(pm, model_p, model_i):
    sm = SearchManager(pm, model_p, model_i, MAX_DEPTH)
    sm.start('DFS', True)
    return sm

def main():
    model_p = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)
    model_p.load_weights(MODEL_P_PATH, by_name=True)
    model_i = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)
    model_i.load_weights(MODEL_I_PATH, by_name=True)
    img = load_img('Data/1.png')
    img = img_to_array(img)
    img_pm = create_init_pm 
    sm = search(img_pm, model_p, model_i)
    sm.solution()

if __name__ == '__main__':
    main()