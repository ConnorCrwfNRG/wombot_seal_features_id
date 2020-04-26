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

cap = cv2.VideoCapture('../videos/tank_features_prcs.mp4')

if (cap.isOpened()== False): 
  print("Error opening video stream or file")
  
  

 

