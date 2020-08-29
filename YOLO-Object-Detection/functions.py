"""Imports"""
import cv2
import matplotlib.pyplot as plt

from utils import *
from darknet import Darknet

from PIL import Image
import os
import image_slicer


"""Setup"""
# Set the location and name of the cfg file
cfg_file = './cfg/yolov3.cfg'
# Set the location and name of the pre-trained weights file
weight_file = './weights/yolov3.weights'
# Set the location and name of the COCO object classes file
namesfile = 'data/coco.names'
# Load the network architecture
m = Darknet(cfg_file)
# Load the pre-trained weights
m.load_weights(weight_file)
# Load the COCO object classes
class_names = load_class_names(namesfile)


def load_and_resize(img_path):
    # Set the default figure size
    plt.rcParams['figure.figsize'] = [24.0, 14.0]

    # Load the image
    img = cv2.imread(img_path)

    # Convert the image to RGB
    original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # We resize the image to the input width and height of the first layer of the network.
    resized_image = cv2.resize(original_image, (m.width, m.height))

    return original_image, resized_image


def single_image(img_path):
    original_image, resized_image = load_and_resize(img_path)

    """Set Thresholds"""
    # Set the NMS threshold
    nms_thresh = 0.6
    # Set the IOU threshold
    iou_thresh = 0.4

    # Detect objects in the image
    boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)

    # Print the objects found and the confidence level
    found = print_objects(boxes, class_names)
    print("===========================")
    print("Found: ", found)
    print("===========================")

    # Plot the image with bounding boxes and corresponding object class labels
    plot_boxes(original_image, boxes, class_names, plot_labels=True)

    return found

def video(video_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
#         print('Read a new frame: ', success)
        count += 1
        if count % 30 == 0:
            single_image('frame%d.jpg' % count)

def crop(img_path, num_squares=9):
    tiles = image_slicer.slice(img_path, num_squares)
    position_labels = {}
    for x, tile in enumerate(tiles):
        single_labels = single_image(tile.filename)
        if x == 1:
            position = 'top left'
            position_labels[position] = set(single_labels)
        if x == 2:
            position = 'top center'
            position_labels[position] = set(single_labels)
        if x == 3:
            position = 'top right'
            position_labels[position] = set(single_labels)
        if x == 4:
            position = 'middle left'
            position_labels[position] = set(single_labels)
        if x == 5:
            position = 'middle center'
            position_labels[position] = set(single_labels)
        if x == 6:
            position = 'middle right'
            position_labels[position] = set(single_labels)
        if x == 7:
            position = 'bottom left'
            position_labels[position] = set(single_labels)
        if x == 8:
            position = 'bottom center'
            position_labels[position] = set(single_labels)
        if x == 9:
            position = 'bottom right'
            position_labels[position] = set(single_labels)
    return position_labels

# single_image('images/mankini.jpg')
# video('images/WAPiro.mp4')
# crop('images/mankini.jpg', num_squares=9)

def analysis(img_path):
    cropped_labels = crop(img_path)
    single_labels = single_image(img_path)
    print(single_labels)
    print(cropped_labels)
    return single_labels, cropped_labels

analysis('images/mankini.jpg')