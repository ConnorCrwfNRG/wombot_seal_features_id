#!/usr/bin/env python

import numpy as np
import cv2
import sys
sys.path.insert(0,'../')
import util

def main():
    image_name = "../images/test_fixture2_sec1.jpg"
    rgb_image = util.read_rgb_image(image_name, True)
    gray_image= util.convert_rgb_to_gray(rgb_image,True)
    binary_image = util.convert_gray_to_binary(gray_image, True, True)
    contours = util.getContours(binary_image)
    util.draw_contours(rgb_image, contours,"RGB Contours")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
