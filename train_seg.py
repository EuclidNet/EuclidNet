import os
import sys
import random
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split

from tensorflow.python.client import device_lib

from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log
import argparse

random.seed(2022)
ROOT_DIR = os.path.abspath("./")
sys.path.append(ROOT_DIR) 
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)
MODEL_NAME = 'mask_rcnn_resnet50_2k.h5'
classes_p = ['Point','Line','Circle']
classes_i = ['LL','LC','CC']

class EuclidNetConfig(Config):
        NAME = "EuclidNet"
        BACKBONE = "resnet101"
        NUM_CLASSES = 1 + len(classes_p)
        GPU_COUNT = 1
        IMAGES_PER_GPU = 2

class EuclidNetDataset(utils.Dataset):
    def load_dataset(self, dataset_dir, txt):
        for idx,label in enumerate(classes_p):
            self.add_class('dataset', idx, label)
        for i, filename in enumerate(os.listdir(dataset_dir)):
            if '.png' in filename and filename in txt:
                self.add_image('dataset', 
                               image_id=i, 
                               path=os.path.join(dataset_dir, filename), 
                               annotation=os.path.join(dataset_dir, filename.replace('.png', '.xml')))
    
    def extract_boxes(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        boxes = []
        classes = []
        for member in root.findall('object'):
            xmin = int(member[4][0].text)
            ymin = int(member[4][1].text)
            xmax = int(member[4][2].text)
            ymax = int(member[4][3].text)
            boxes.append([xmin, ymin, xmax, ymax])
            classes.append(self.class_names.index(member[0].text))
        width = int(root.find('size')[0].text)
        height = int(root.find('size')[1].text)
        return boxes, classes, width, height
 
    def load_mask(self, image_id):
        info = self.image_info[image_id]
        path = info['annotation']
        boxes, classes, w, h = self.extract_boxes(path)
        masks = np.zeros([h, w, len(boxes)], dtype='uint8')
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
        return masks, np.asarray(classes, dtype='int32')
    
    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']

class InferenceConfig(EuclidNetConfig):
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

def train(dataset_train, dataset_val):   
    config = EuclidNetConfig()
    config.display()

    model = modellib.MaskRCNN(mode="training", config=config,
                            model_dir=MODEL_DIR)

    model.train(dataset_train, dataset_val, 
                learning_rate=config.LEARNING_RATE, 
                epochs=200, 
                layers='heads')

    model.train(dataset_train, dataset_val, 
                learning_rate=config.LEARNING_RATE / 10,
                epochs=50, 
                layers="all")

    model_path = os.path.join('./', MODEL_NAME)
    model.keras_model.save_weights(model_path)

def inference(dataset_val):  
    inference_config = InferenceConfig()

    model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)
    model_path = os.path.join(ROOT_DIR, MODEL_NAME)
    print("Loading weights from ", model_path)
    model.load_weights(model_path, by_name=True)

    def get_ax(rows=1, cols=1, size=8):
        _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
        return ax

    model = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)
    model_path = os.path.join(ROOT_DIR,MODEL_NAME)
    print("Loading weights from ", model_path)
    model.load_weights(model_path, by_name=True)
    image_id = random.choice(dataset_val.image_ids)
    original_image, image_meta, gt_class_id, gt_bbox, gt_mask = modellib.load_image_gt(dataset_val, inference_config,image_id, use_mini_mask=False)
    image_ids = dataset_val.image_ids
    app = [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]
    APs = []
    precisionss = []
    recallss = []
    overlapss = []
    all_apps = []
    for apd in app:
        for image_id in image_ids:
            image, image_meta, gt_class_id, gt_bbox, gt_mask = modellib.load_image_gt(dataset_val, inference_config,
                                                                                    image_id, use_mini_mask=False)
            molded_images = np.expand_dims(modellib.mold_image(image, inference_config), 0)
            results = model.detect([image], verbose=0)
            r = results[0]
            AP, precisions, recalls, overlaps = utils.compute_ap(gt_bbox, gt_class_id, gt_mask,
                                                                r["rois"], r["class_ids"], r["scores"], r['masks'],iou_threshold=apd)
            APs.append(AP)

        print("mAP: ", np.mean(APs))
        all_apps.append(np.mean(APs))
    print('Backbone: resnet101')#resnet50
    print('AP: ', np.mean(all_apps))
    print('AP@0.5: ', all_apps[0])
    print('AP@0.75:',all_apps[5])

def main():
    data_txt = []
    data_path = 'Data/Extraction'
    for i, filename in enumerate(os.listdir(data_path)):
            if '.png' in filename:
                data_txt.append(filename)
    train_txt, test_txt = train_test_split(data_txt, test_size=0.15, random_state = 2022)
    print(len(train_txt))
    print(len(test_txt))
    dataset_train = EuclidNetDataset()
    dataset_train.load_dataset(data_path, train_txt)
    dataset_train.prepare()
    print('Train size: %d' % len(dataset_train.image_ids))
    
    dataset_val = EuclidNetDataset()
    dataset_val.load_dataset(data_path,test_txt)
    dataset_val.prepare()
    print('Test size: %d' % len(dataset_val.image_ids))

    train(dataset_train, dataset_val)
    inference(dataset_val)

if __name__ == "__main__":
    main()
