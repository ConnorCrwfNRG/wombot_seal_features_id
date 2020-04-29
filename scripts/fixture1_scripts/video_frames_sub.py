#!/usr/bin/env python
     
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

#adds parents directory to python path. only works if run through terminal or pycharm
#for roslaunch you need to explicitly type the specific PYTHONPATH to capture util.py
#still need to figure out how to add gradparents directory to path
import sys
print(sys.path)
sys.path.insert(0,'../')
# or to append
# sys.path.append('../')
print(sys.path)
# or longer way is
# import os.path, sys
# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
# print(sys.path)

import util

# this is the module __init__.py way to do it
# import scripts.util as util
# from scripts import util

bridge = CvBridge()
img_counter = 0

def image_callback(ros_image):
  # print 'got an image'
  global bridge
  global img_counter
  #convert ros_image into an opencv-compatible image
  try:
    cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
    print(e)
  #from now on, you can work exactly like with opencv
  cv2.imshow("test", cv_image)
  img_name = "test_piece_{}.png".format(img_counter)
  if cv2.waitKey(33) == ord('s'):
    new_img_counter = util.capture_frame(cv_image, img_name, img_counter)
    img_counter = new_img_counter
  cv2.waitKey(1)
    
def main():
  rospy.init_node('video_frames_sub', anonymous=True)
  image_sub = rospy.Subscriber("video_frames", Image, image_callback)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()