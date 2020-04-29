#!/usr/bin/env python

import numpy as np
import cv2
import sys
sys.path.insert(0,'../')
import util

def main():
    image_name = "../images/test_fixture2_sec1.jpg"
    rgb_image = util.read_rgb_image(image_name, False)
    height, width, _ = util.get_image_size(rgb_image)
    gray_image= util.convert_rgb_to_gray(rgb_image,False)
    binary_image = util.convert_gray_to_binary(gray_image, True, False)
    contours = util.get_contours(binary_image)
    contours_properties = util.get_contours_info(contours)
    filtered_properties = util.filter_contours_pos(contours_properties, 700, 20000)
    util.draw_contours(rgb_image, binary_image, filtered_properties)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
