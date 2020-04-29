# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 19:38:27 2020

@author: Henry Jiang
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:24:19 2020

@author: Henry Jiang
"""

import cv2
import numpy as np
import argparse
import imutils
import time
import os

# Create a VideoCapture object and read from input file

# If the input is the camera, pass 0 instead of the video file name

path = os.path.join( os.getcwd(), '..', 'videos\Test_Video_WHoles.mov' )

cap = cv2.VideoCapture(path)             
             
#cap = cv2.VideoCapture('..\videos\Test_Video_WHoles.mov')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
 
        # Display the resulting frame
        # convert the frame to grayscale, blur it, and detect edges
        width = 600
        height = 600
        upper_bound = height-100
        lower_bound = height
        left_bound = 0 
        right_bound = width 
        frame = cv2.resize(frame, (width,height))
        RIO = frame[upper_bound:height,left_bound:right_bound]
        cv2.rectangle(frame, (0, upper_bound), (right_bound, height), (0, 255, 0), 2)
        
        
        
        ## Gray for RIO
        gray = cv2.cvtColor(RIO, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        #edged = cv2.Canny(blurred, 50, 150)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
        ret,thresh1 = cv2.threshold(blurred,140,255,cv2.THRESH_BINARY_INV)
        edged = cv2.Canny(thresh1, 50, 150)
        cv2.imshow('Threshold', thresh1)

        cv2.imshow('Edged', edged)
        cv2.imshow('Blurred', blurred)
        
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = imutils.grab_contours(cnts)
        left_point = []
        right_point = []
        
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            #print(peri)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)
            #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w/h;
            
            if w > 200 and h < 50 and aspect_ratio > 10:
                
                # Drawing over the countour
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                
                #fitting a bouding rectangle
                #rect = cv2.minAreaRect(c)
                #box = cv2.boxPoints(rect)
                #box = np.int0(box)
                #im = cv2.drawContours(frame,[box],0,(0,0,255),2)

                
                rows,cols = frame.shape[:2]
                [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
                lefty = int((-x*vy/vx) + y)
                lefty = lefty + upper_bound
                left_point.append((left_bound,lefty))
                righty = int(((cols-x)*vy/vx)+y)
                righty = righty + upper_bound
                right_point.append((right_bound,righty))
                
                img = cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)
                
        ### Code to connect points goes here
        if len(left_point) ==2 and len(right_point)==2:
            left = cv2.line(frame, left_point[0], left_point[1], (0,0,255), 2)
            left_dist = float(abs(left_point[0][1] - left_point[1][1])) / 10
            
            right = cv2.line(frame, right_point[0], right_point[1], (0,0,255), 2)
            right_dist = float(abs(right_point[0][1] - right_point[1][1])) / 10
            print(left_point, right_point)
            cv2.putText(frame, 'The left distance is ' + str(left_dist) + ' cm', (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0,255,0), 2)
            cv2.putText(frame, 'The right distance is ' + str(right_dist) + ' cm', (50,100), cv2.FONT_HERSHEY_SIMPLEX , 1, (0,255,0), 2)
        cv2.imshow('Frame',frame)
 
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

  # Break the loop
    else: 
        break

 

# When everything done, release the video capture object
cap.release()

 
# Closes all the frames
cv2.destroyAllWindows()


 

