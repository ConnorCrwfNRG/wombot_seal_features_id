#!/usr/bin/env python 

import cv2
import sys

def main(cap):
	while(cap.isOpened()== True):
		ret, frame = cap.read()
		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = cv2.resize(frame, (0,0), fx=0.5,fy=0.5)
		#cv2.line(frame,(0,0),(511,511),(255,0,0),5)
		cv2.imshow("Frame",frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	print("Video has ended")
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	print(sys.argv)
	# video_capture = cv2.VideoCapture(0)
	video_capture = cv2.VideoCapture('../videos/seal_vid1.mp4')
	main(video_capture)