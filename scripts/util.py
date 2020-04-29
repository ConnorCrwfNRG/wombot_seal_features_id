#!/usr/bin/env python
import numpy as np
import cv2
import os

#brouht in from image_thresholding.py

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

def get_contours(binary_image):
    _, contours, hierarchy = cv2.findContours(binary_image,
                                              cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
    print ("number of contours: {}".format(len(contours)))
    return contours

def draw_contours(rgb_image, binary_image, all_properties):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1], 3], 'uint8')
    index = -1 #means all contours
    thickness = 1 #thinkess of the contour line
    contour_color = (150, 250, 150)  #color of the contour line
    circle_color = (0, 0, 255)
    for c_prcs in all_properties:
        cv2.drawContours(rgb_image, [c_prcs['Raw_Data']], index, contour_color, thickness)
        cv2.drawContours(black_image, [c_prcs['Raw_Data']], index, contour_color, thickness)
        cv2.circle(rgb_image, (c_prcs['X_Pos_Ctr'], c_prcs['Y_Pos_Ctr']), c_prcs['Rad'], circle_color, 1)
        cv2.circle(black_image, (c_prcs['X_Pos_Ctr'], c_prcs['Y_Pos_Ctr']), c_prcs['Rad'], circle_color, 1)
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)


# brought in from contours_processing.py example

def get_contours_info(contours):
    all_properties = []
    # print(type(contours)) -> list
    for c_raw in contours:
        properties = {}
        # print(type(c_raw)) -> numpy.ndarray
        area = cv2.contourArea(c_raw)
        perimeter = cv2.arcLength(c_raw, True)
        circle_pos, circle_rad = cv2.minEnclosingCircle(c_raw)
        properties['Raw_Data'] = c_raw
        properties['Area'] = area
        properties['Perim'] = perimeter
        properties['X_Pos'] = int(circle_pos[0])
        properties['Y_Pos'] = int(circle_pos[1])
        properties['Rad'] = int(circle_rad)
        properties['X_Pos_Ctr'], properties['Y_Pos_Ctr'] = get_contour_center(c_raw)
        # print ("Area: {}, Perimeter: {}".format(area, perimeter))
        # print(properties)
        all_properties.append(properties)
    return all_properties


def get_contour_center(contour):
    M = cv2.moments(contour)
    cx = -1
    cy = -1
    if (M['m00'] != 0):
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    return cx, cy

# connor's added functions

def get_image_size(img):
    # get dimensions of image
    dimensions = img.shape

    # height, width, number of channels in image
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    print('Image Dimension    : ', dimensions)
    print('Image Height       : ', height)
    print('Image Width        : ', width)
    print('Number of Channels : ', channels)

    return height, width, channels

def filter_contours_pos(properties_all,y_pos_max,area_max):
    criteria_count = 0
    filtered_properties = []
    for c_prcs in properties_all:
        if c_prcs['Y_Pos_Ctr'] > y_pos_max and c_prcs['Area'] > area_max:
            criteria_count += 1
            print("Area of this contour is: %d" % c_prcs['Area'])
            print("X_Pos_Ctr of this contour is: %d" % c_prcs['X_Pos_Ctr'])
            print("Y_Pos_Ctr of this contour is: %d" % c_prcs['Y_Pos_Ctr'])
            filtered_properties.append(c_prcs)
    print "Number of contours matching criteria: %d" % criteria_count
    return filtered_properties
