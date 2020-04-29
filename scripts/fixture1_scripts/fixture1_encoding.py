#!/usr/bin/env python 

import numpy as np
import cv2
from scripts import util

image_name = "fixture"
fixture_num=1

print('read an image from file')
color_image = cv2.imread("../../images/fixture1.png",cv2.IMREAD_COLOR)

print('display image in native color')
cv2.imshow("Original Image",color_image)
cv2.moveWindow("Original Image",0,0)
print(color_image.shape)

height,width,channels = color_image.shape

print('slipt the image into three channels.')
blue,green,red = cv2.split(color_image)

cv2.imshow("Blue Channel",blue)
cv2.moveWindow("Blue Channel",0,height)

cv2.imshow("Red Channel",red)
cv2.moveWindow("Red Channel",0,height)

cv2.imshow("Greeen Channel",green)
cv2.moveWindow("Green Channel",0,height)


# Hue: indicates the type of color that we see in a 360 degree format.
# Saturation: an indication of how saturated an individual color is 
# Value: indicates how luminous the channel is. 

print('---- convert color image to HSV format----- ')
hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
hsv_image = np.concatenate((h,s,v),axis=1)
cv2.imshow("HSV Image",hsv)
cv2.imshow("HSV Image Channel Split",hsv_image)


print('---- Saturation channel output----- ')
img_name = "%s%s_saturation.png" %(image_name, fixture_num)
#only uses the s channel in what it shows and captures
cv2.imshow("Saturation Channel",s)
util.capture_frame(s, img_name, fixture_num)


print('------ converts an image to a grayscale ------')
gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Image ",gray_image)
img_name = "%s%s_gray.png" %(image_name, fixture_num)
util.capture_frame(gray_image, img_name, fixture_num)

print(gray_image)

cv2.waitKey(0)
cv2.destroyAllWindows()