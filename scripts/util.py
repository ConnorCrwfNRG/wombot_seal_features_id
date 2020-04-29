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

def convert_gray_to_binary_basicThresh(gray_image, threshol_value,show):
    ret, thresh_basic = cv2.threshold(gray_image,threshol_value,255,cv2.THRESH_BINARY_INV)
    if show:
        cv2.imshow("Basic Binary Image",thresh_basic)
    return thresh_basic

def adaptive_thresholding(image, threshol_value):
    adaptive_threshold_image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,threshol_value,2)
    cv2.imshow("Adaptive Threshold Image",adaptive_threshold_image)

# brought in from contours_detection.py example

def read_starting_image(image_name, show):
    image = cv2.imread(image_name)
    if show:
        cv2.imshow("Starting Image",image)
    return image

def convert_rgb_to_gray(rgb_image,show):
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    if show:
        cv2.imshow("Gray Image",gray_image)
    return gray_image

def convert_gray_to_binary_adaptiveThresh(gray_image, adaptive, show):
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

def draw_contours(rgb_image, binary_image, filtered_contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1], 3], 'uint8')
    index = -1 #means all contours
    thickness = 1 #thinkess of the contour line
    contour_color = (150, 250, 150)  #color of the contour line
    circle_color = (0, 0, 255)
    for c_prcs in filtered_contours:
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

def filter_contours_minValue(properties_all, **kwargs):
    all_criteria_met_count = 0
    kwargs_len = len(kwargs)
    filtered_contours = []
    for c_prcs in properties_all:
        pass_count = 0
        for key, value in kwargs.items():
            if c_prcs[key] > value:
                pass_count += 1
        if pass_count == kwargs_len:
            print("Area of this contour is: %d" % c_prcs['Area'])
            print("Perimeter of this contour is: %d" % c_prcs['Perim'])
            print("Center X Position of this contour is: %d" % c_prcs['X_Pos_Ctr'])
            print("Center Y Position of this contour is: %d" % c_prcs['Y_Pos_Ctr'])
            filtered_contours.append(c_prcs)
            all_criteria_met_count += 1
    print "Number of contours matching criteria: %d" % all_criteria_met_count
    return filtered_contours

#after running a canny edge detection, there is a good chance that when you get_contours,
#you will find some contours with zero area. will just have to use perimeter as a criteria filter instead
def canny_edge(image, thresh1, thresh2, show):
    canny_edge_image = cv2.Canny(image, thresh1, thresh2)
    if show:
        cv2.imshow("Canny Edge Image",canny_edge_image)
    return canny_edge_image

def get_contours_options(binary_image,retr_option,chain_option):
    #could also do kwargs for this with something liek the following
    #if 'retr_option' in kwargs.keys() and 'chain_option' in kwargs.keys():
    _, contours, hierarchy = cv2.findContours(binary_image,
                                              retr_option,
                                               chain_option)
    print ("Number of Contours: {}".format(len(contours)))
    # or
    # print("Number of Contours found = " + str(len(contours)))
    return contours

def convert_rgb_to_hsv(rgb_image,show):
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hsv_image = np.concatenate((h, s, v), axis=1)
    if show:
        cv2.imshow("HSV Image",hsv_image)
    return h,s,v

def draw_contours_coordinates(binary_image, filtered_contours):
    img_height = binary_image.shape[0]
    img_width = binary_image.shape[1]
    black_image = np.zeros([img_height, img_width, 3], 'uint8')
    print("Width by Height of image is: {} by {}".format(img_width,img_height))
    index = 0  # means all contours
    thickness = 5  # thinkess of the contour line
    contour_color = (0, 0, 255)  # color of the contour line
    for c_prcs in filtered_contours:
        approx = cv2.approxPolyDP(c_prcs['Raw_Data'], 0.009 * cv2.arcLength(c_prcs['Raw_Data'], True), True)
        cv2.drawContours(black_image, [approx], index, contour_color, thickness)
        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel()
        print(np.size(n))
        print(n)
        n = n.tolist()
        print(n)
        # i = 0
        font = cv2.FONT_HERSHEY_COMPLEX
        for j in n:
            i = n.index(j)
            if (i % 2 == 0):
                x = n[i]
                y = n[i + 1]
                # String containing the co-ordinates.
                string = "(" + str(x) + "," + str(y) + ")"
                #checks to see if placement of text in the x position is out of bounds of the image
                if (img_width-x) < 75:
                    x_locate = x - 75
                    y_locate = y - 25
                else:
                    x_locate = x
                    y_locate = y - 10
                # check if x is the far-right point of the contour, display it differently if so
                if (i == 0):
                    cv2.putText(black_image, "Arrow tip", (x_locate, y_locate),
                                font, 0.5, (255, 0, 0))
                    cv2.putText(black_image, string, (x_locate, y_locate+25),
                                font, 0.5, (0, 255, 0))
                else:
                    # text on remaining co-ordinates.
                    cv2.putText(black_image, string, (x_locate, y_locate),
                                font, 0.5, (0, 255, 0))
    cv2.imshow("Black Image Contours with Coordinates", black_image)
