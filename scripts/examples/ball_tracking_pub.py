#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
 
bridge = CvBridge()
 
 
def read_publish():
  global bridge
  global loop_rate
 
  loop_rate = rospy.Rate(30)
  video_capture = cv2.VideoCapture(1)
  publisher = rospy.Publisher("tennis_ball_image", Image, queue_size=10)
 
  while(video_capture.isOpened()):
    ret, rgb_image = video_capture.read()
    if not ret:
      continue
    try:
      ros_image = bridge.cv2_to_imgmsg(rgb_image, "bgr8")
    except CvBridgeError as e:
      print(e)
      continue
    except KeyboardInterrupt:
      print("Shutting down")
      video_capture.release()
        
    publisher.publish(ros_image)
    loop_rate.sleep()
 
  
def main():
  rospy.init_node('image_publisher', anonymous=True)
  try:
    read_publish()
  except KeyboardInterrupt:
    print("Shutting down")
 
if __name__ == '__main__':
    main()