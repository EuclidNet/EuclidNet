import os
import cv2
import numpy as np
import shutil
import random
import argparse
from pascal_voc_writer import Writer
from matplotlib import pyplot as plt
random.seed(2022)

def compute_iou(box1, box2):
    """xmin, ymin, xmax, ymax"""

    A1 = (box1[2] - box1[0])*(box1[3] - box1[1])
    A2 = (box2[2] - box2[0])*(box2[3] - box2[1])

    xmin = max(box1[0], box2[0])
    ymin = max(box1[1], box2[1])
    xmax = min(box1[2], box2[2])
    ymax = min(box1[3], box2[3])

    if ymin >= ymax or xmin >= xmax: return 0
    return  ((xmax-xmin) * (ymax - ymin)) / (A1 + A2)

def make_point(data):
    blank = data[0]
    boxes = data[1]
    label = data[2]
    ID = 'Point'
    image = np.zeros((21,21,3),dtype=np.uint8)
    image.fill(255)
    cv2.circle(image, (10,10), 10 , (56, 56, 56), -1)
    h, w, c = image.shape
    while True:
        xmin = np.random.randint(0, SIZE-w, 1)[0]
        ymin = np.random.randint(0, SIZE-h, 1)[0]
        xmax = xmin + w
        ymax = ymin + h
        box = [xmin, ymin, xmax, ymax]

        iou = [compute_iou(box, b) for b in boxes]
        if max(iou) < 0.02:
            boxes.append(box)
            label.append(ID)
            break

    for i in range(w):
        for j in range(h):
            x = xmin + i
            y = ymin + j
            blank[y][x] = image[j][i]
    # cv2.rectangle(blank, (xmin, ymin), (xmax, ymax), [0, 0, 255], 2)
    return blank

def make_line(data):
    blank = data[0]
    boxes = data[1]
    label = data[2]
    ID = 'Line'
    l_w = random.randint(10, 200)
    l_h = random.randint(10, 200)

    h_v = random.randint(0, 1)# 0: horizontial 1:vertical
    if h_v == 0:
        image = np.zeros((21,l_h+11,3),dtype=np.uint8)
        image.fill(255)
        cv2.line(image, (10,10), (l_h,10) , (56, 56, 56), 5)
        cv2.circle(image, (10,10), 10 , (56, 56, 56), -1)
        cv2.circle(image, (l_h,10), 10 , (56, 56, 56), -1)
    else:
        image = np.zeros((l_w+11,21,3),dtype=np.uint8)
        image.fill(255)
        cv2.line(image, (10,10), (10,l_w) , (56, 56, 56), 5)
        cv2.circle(image, (10,10), 10 , (56, 56, 56), -1)
        cv2.circle(image, (10,l_w), 10 , (56, 56, 56), -1)
    
    h, w, c = image.shape
    while True:
        xmin = np.random.randint(0, SIZE-w, 1)[0]
        ymin = np.random.randint(0, SIZE-h, 1)[0]
        xmax = xmin + w
        ymax = ymin + h
        box = [xmin, ymin, xmax, ymax]

        iou = [compute_iou(box, b) for b in boxes]
        if max(iou) < 0.02:
            boxes.append(box)
            label.append(ID)
            break

    for i in range(w):
        for j in range(h):
            x = xmin + i
            y = ymin + j
            blank[y][x] = image[j][i]
    # cv2.rectangle(blank, (xmin, ymin), (xmax, ymax), [0, 0, 255], 2)
    return blank

def make_circle(data):
    blank = data[0]
    boxes = data[1]
    label = data[2]
    ID = 'Circle'
    radius = random.randint(10, 100)
    image = np.zeros((radius*2+10,radius*2+10,3),dtype=np.uint8)
    image.fill(255)
    cv2.circle(image, (radius+5,radius+5), radius , (56, 56, 56), 5)
#     h_v = random.randint(0, 1)# 0: horizontial 1:vertical
#     if h_v == 0:
#         image = np.zeros((21,l_h+11,3),dtype=np.uint8)
#         image.fill(255)
#         cv2.line(image, (10,10), (l_h,10) , (56, 56, 56), 5)
#         cv2.circle(image, (10,10), 10 , (56, 56, 56), -1)
#         cv2.circle(image, (l_h,10), 10 , (56, 56, 56), -1)
#     else:
#         image = np.zeros((l_w+11,21,3),dtype=np.uint8)
#         image.fill(255)
#         cv2.line(image, (10,10), (10,l_w) , (56, 56, 56), 5)
#         cv2.circle(image, (10,10), 10 , (56, 56, 56), -1)
#         cv2.circle(image, (10,l_w), 10 , (56, 56, 56), -1)
#     plt.imshow(image)
#     plt.show()
    h, w, c = image.shape
    while True:
        xmin = np.random.randint(0, SIZE-w, 1)[0]
        ymin = np.random.randint(0, SIZE-h, 1)[0]
        xmax = xmin + w
        ymax = ymin + h
        box = [xmin, ymin, xmax, ymax]

        iou = [compute_iou(box, b) for b in boxes]
        if max(iou) < 0.02:
            boxes.append(box)
            label.append(ID)
            break

    for i in range(w):
        for j in range(h):
            x = xmin + i
            y = ymin + j
            blank[y][x] = image[j][i]
    # cv2.rectangle(blank, (xmin, ymin), (xmax, ymax), [0, 0, 255], 2)
    return blank
    
def main():
    SIZE = 512
    NUM_IMG = 1000
    images_path = './Data/Extraction/'
    for idx in range(783,NUM_IMG):
        image_path = os.path.realpath(os.path.join(images_path, "%04d.png" %(idx+1)))
        img = np.ones(shape=[SIZE, SIZE, 3]) * 255
        bboxes = [[0,0,1,1]]
        labels = [0]
        data = [img, bboxes, labels]
        bboxes_num = 0

        N_p = random.randint(1, 11)
        N_l = random.randint(0, 5)
        N_c = random.randint(0, 3)

        for _ in range(N_p):
            data[0] = make_point(data)

        for _ in range(N_l):
            data[0] = make_line(data)

        for _ in range(N_c):
            data[0] = make_circle(data)

        # print(labels)
        # plt.imshow(data[0])
        # plt.show()
        cv2.imwrite(image_path, data[0])
        writer = Writer(image_path, SIZE, SIZE)
        for i in range(len(labels)):
                    if i == 0: continue
                    xmin = str(bboxes[i][0])
                    ymin = str(bboxes[i][1])
                    xmax = str(bboxes[i][2])
                    ymax = str(bboxes[i][3])
                    class_ind = str(labels[i])
                    writer.addObject(class_ind, xmin, ymin, xmax, ymax)
        writer.save(image_path.split('.')[0]+'.xml')
        if idx%50==0:
            print('Processed #{}.png'.format(idx))

if __name__ == '__main__':
    main()