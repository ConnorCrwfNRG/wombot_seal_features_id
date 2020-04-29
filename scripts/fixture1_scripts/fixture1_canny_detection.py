#!/usr/bin/env python 
import cv2

gray_img = cv2.imread("../../images/fixture1_gray.png")
saturation_img = cv2.imread("../../images/fixture1_saturation.png")

#cv2.imshow("Gray Image", gray_img)
#cv2.imshow("Saturation Image", saturation_img)
 
edge_img_gray = cv2.Canny(gray_img,100,200)
edge_img_saturation = cv2.Canny(saturation_img,100,200)
 
#cv2.imshow("Detected Edges (Gray)", edge_img_gray)
#cv2.imshow("Detected Edges (Saturation)", edge_img_saturation)

threshol_value=115
#thresh_basic = util.convert_gray_to_binary_basicThresh(gray_img,threshol_value)
edge_img_basic = cv2.Canny(gray_img,100,200)
#cv2.imshow("Detected Edges (Basic)", edge_img_basic)

cv2.imshow('Canny Edges Before Contouring', edge_img_saturation) 

# Finding Contours 
# Use a copy of the image e.g. edged.copy() 
# since findContours alters the image 
_, contours, hierarchy = cv2.findContours(edge_img_saturation,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
  
print("Number of Contours found = " + str(len(contours))) 

max_perimeter = 0
for c in contours:
# This is to ignore that small hair countour which is not big enough
     new_perimeter = cv2.arcLength(c,True)
     if new_perimeter>max_perimeter:
        max_perimeter = new_perimeter
         #max_cnt = max(cnts, key = cv2.contourArea)
        max_cnt = c
    # compute the bounding box of the of the paper region and return it
    #print("Min Area Rect is: {}" .format(cv2.minAreaRect(c)))
print(cv2.arcLength(max_cnt,True))
#if (perimeter>1000):
cv2.drawContours(saturation_img, [max_cnt], -1, (150,250,150), 3)
cv2.imshow('Longest Contour', saturation_img) 
  
# Draw all contours 
# -1 signifies drawing all contours 
#cv2.drawContours(saturation_img, contours, -1, (0, 255, 0), 3) 
#cv2.imshow('Contours', saturation_img) 

max_perimeter =1000
contour_list = []
i = 0
for c in contours:
# This is to ignore that small hair countour which is not big enough
    test_perimeter = cv2.arcLength(c,True)
    if test_perimeter>max_perimeter:
        contour_list.insert(i, c)
        cv2.drawContours(saturation_img, [c], -1, (150,250,150), 3)
        i+=1
        #contour_list.append[c]
    # compute the bounding box of the of the paper region and return it
    #print("Min Area Rect is: {}" .format(cv2.minAreaRect(c)))
print(len(contour_list))
print(i)
cv2.imshow('Three Contours', saturation_img) 

for cnt in contour_list: 
  
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
  
    # draws boundary of contours. 
    cv2.drawContours(saturation_img, [approx], 0, (0, 0, 255), 5)  
  
    # Used to flatted the array containing 
    # the co-ordinates of the vertices. 
    n = approx.ravel()  
    i = 0
  
    font = cv2.FONT_HERSHEY_COMPLEX
    
    for j in n : 
        if(i % 2 == 0): 
            x = n[i] 
            y = n[i + 1] 
  
            # String containing the co-ordinates. 
            string = str(x) + " " + str(y)  
  
            if(i == 0): 
                # text on topmost co-ordinate. 
                cv2.putText(saturation_img, "Arrow tip", (x, y), 
                                font, 0.5, (255, 0, 0))  
            else: 
                # text on remaining co-ordinates. 
                cv2.putText(saturation_img, string, (x, y),  
                          font, 0.5, (0, 255, 0))  
        i = i + 1
cv2.imshow('Contour Coordinates', saturation_img) 

cv2.waitKey(0) 
cv2.destroyAllWindows() 