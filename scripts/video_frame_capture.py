#!/usr/bin/env python

import cv2
import imutils

key = cv2.waitKey(1)
# video = cv2.VideoCapture(0)
video = cv2.VideoCapture('../videos/seal_vid2.mp4')

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.

capture_video = False
if capture_video == True:
    out = cv2.VideoWriter('../videos/seal_vid2_rotated.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (600,600))
while True:
    try:
        check, frame = video.read()
        print(check)  # prints true as long as the webcam is running
        print(frame)  # prints matrix values of each framecd
        frame = imutils.rotate(frame,90)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        frame = cv2.resize(frame, (600, 600))
        cv2.imshow("Capturing", frame)
        if capture_video == True:
            out.write(frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            video.release()
            img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
            img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            print("Converting RGB image to grayscale...")
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            print("Converted RGB image to grayscale...")
            print("Resizing image to 28x28 scale...")
            img_ = cv2.resize(gray, (28, 28))
            print("Resized...")
            img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            print("Image saved!")

            break
        elif key == ord('q'):
            print("Turning off camera.")
            video.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

    except(KeyboardInterrupt):
        print("Turning off camera.")
        video.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break