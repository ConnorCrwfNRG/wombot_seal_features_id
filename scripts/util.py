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

