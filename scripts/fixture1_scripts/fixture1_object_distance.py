#!/usr/bin/env python
# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
import time
import sys
sys.path.insert(0,'../')
import util
 
def find_focalLength(frame):

    try:
        marker = find_marker(frame)
        area = marker[1][0]*marker[1][1]
        if area>11000:
            box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
            box = np.int0(box)
            cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv2.imshow('calibration', frame) # show frame on window
        #return (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        return (marker[1][1] * KNOWN_DISTANCE) / KNOWN_HEIGHT
    except:
        pass

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

def filter_color(rgb_old, lower_bound, upper_bound):
    #convert the image into the HSV color space
    hsv_image = cv2.cvtColor(rgb_old, cv2.COLOR_BGR2HSV)
    #define a mask using the lower and upper bounds of the yellow color 
    hsv_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    return hsv_image, hsv_mask

def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    print(image.shape)
    greenLower_below = (0, 0, 0)
    greenUpper_below = (60, 150, 200)
    greenLower_above = (90, 0, 0)
    greenUpper_above = (180, 150, 200)
    hsv_image, hsv_mask_below = filter_color(image,greenLower_below,greenUpper_below)
    hsv_image, hsv_mask_above = filter_color(image,greenLower_above,greenUpper_above)
    hsv_mask = cv2.bitwise_or(hsv_mask_below, hsv_mask_above)
    hsv_bitwise = cv2.bitwise_and(hsv_image, hsv_image, mask = hsv_mask)
    #bring it back to rgb
    rgb_new = cv2.cvtColor(hsv_bitwise,cv2.COLOR_HSV2BGR)
    cv2.imshow("rgb_new",rgb_new)
    gray = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)
    #ret2,th2 = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #kernel = np.ones((8,8), np.uint8)
    edged = cv2.Canny(blurred, 85, 255)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    #edged = auto_canny(blurred)
    cv2.imshow("intermediate_image", edged)

    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    max_area = 0
    for c in cnts:
    # This is to ignore that small hair countour which is not big enough
        new_area = cv2.contourArea(c)
        if new_area>max_area:
            max_area = new_area
            #max_cnt = max(cnts, key = cv2.contourArea)
            max_cnt = c
    # compute the bounding box of the of the paper region and return it
    #print("Min Area Rect is: {}" .format(cv2.minAreaRect(c)))
    return cv2.minAreaRect(max_cnt)
    
def distance_to_camera(knownDim, focalLength, perDim):
	# compute and return the distance from the maker to the camera
    return (knownDim * focalLength) / perDim
   

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 16
 
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 10
KNOWN_HEIGHT = 7

def main():
    # video_capture = cv2.VideoCapture(2)
    #video_capture = cv2.VideoCapture('video/tennis-ball-video.mp4')
    image_name = "../../images/fixture1.png"
    frame = util.read_starting_image(image_name, False)

    # load the first image that contains an object that is KNOWN TO BE 2 feet
    # from our camera, then find the paper marker in the image, and initialize
    # the focal length for use in while loopo
    t_end = time.time() + 5
    while time.time() < t_end:
        print("calibrating...")
        # frames_per_sec = video_capture.get(cv2.CAP_PROP_FPS)
        #print ("frames per second: {}".format(frames_per_sec))
        # frame_no = 0.01
        # cap.set(2,frame_no) #setting doesn't work for videoCapture, just videos
        # ret1, frame1 = video_capture.read() # Read the frame
        focalLength_initial = find_focalLength(frame)
        time.sleep(.033)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("done calibrating")
    print("Focal Length is: {}" .format(focalLength_initial))

    while(True):
        # now after calibration, load the image, find the marker in the image, then compute the
	    # distance to the marker from the camera

        # ret, frame = video_capture.read()
        try:
            marker = find_marker(frame)
            area = marker[1][0]*marker[1][1]
            #inches = distance_to_camera(KNOWN_WIDTH, focalLength_initial, marker[1][0])
            inches = distance_to_camera(KNOWN_HEIGHT, focalLength_initial, marker[1][1])
            # draw a bounding box around the frame and display it
            if area > 1100:
                box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
                box = np.int0(box)
                cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
            cv2.putText(frame, "%.2fft" % (inches / 12),
            (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)
        except:
            pass
	    
        cv2.imshow("frame",frame)
        time.sleep(.033)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()


cv2.waitKey(0)
cv2.destroyAllWindows()