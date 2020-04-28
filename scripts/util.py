#!/usr/bin/env python
import cv2
import os

def capture_frame(frame, name, counter):
    path = './'
    #print(os.path.join(path , img_name))
    cv2.imwrite(os.path.join(path , name), frame)
    print("{} written!".format(name))
    counter += 1
    return counter

def basic_thresholding(gray_image, threshol_value):
    ret, thresh_basic = cv2.threshold(gray_image,threshol_value,255,cv2.THRESH_BINARY_INV)
    cv2.imshow("Basic Binary Image",thresh_basic)
    return thresh_basic

def adaptive_thresholding(image, threshol_value):
    adaptive_threshold_image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,threshol_value,2)
    cv2.imshow("Adaptive Threshold Image",adaptive_threshold_image)

# brought in from contours_detection.py example

def read_rgb_image(image_name, show):
    rgb_image = cv2.imread(image_name)
    if show:
        cv2.imshow("RGB Image",rgb_image)
    return rgb_image

def convert_rgb_to_gray(rgb_image,show):
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    if show:
        cv2.imshow("Gray Image",gray_image)
    return gray_image

def convert_gray_to_binary(gray_image, adaptive, show):
    if adaptive:
        binary_image = cv2.adaptiveThreshold(gray_image,
                            255,
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY_INV, 115, 2)
    else:
        _,binary_image = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)
    if show:
        cv2.imshow("Binary Image", binary_image)
    return binary_image

def getContours(binary_image):
    _, contours, hierarchy = cv2.findContours(binary_image,
                                              cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(image, contours, image_name):
    index = -1 #means all contours
    thickness = 2 #thinkess of the contour line
    color = (255, 0, 255) #color of the contour line
    cv2.drawContours(image, contours, index, color, thickness)
    cv2.imshow(image_name,image)
