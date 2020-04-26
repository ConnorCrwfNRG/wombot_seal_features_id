#!/usr/bin/env python
     
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from scripts import util

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
  if cv2.waitKey(33) == ord('a'):
    new_img_counter = util.capture_img(cv_image, img_name, img_counter)
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