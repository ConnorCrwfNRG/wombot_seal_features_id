#!/usr/bin/env python

import numpy as np
import cv2
import scripts.util as util
# or can do
#import sys
#sys.path.insert(0,'../')
#import util

def main():
    image_name = "../../images/fixture1.png"
    rgb_image = util.read_starting_image(image_name, False)
    gray_image = util.convert_rgb_to_gray(rgb_image,False)
    binary_image = util.convert_gray_to_binary_basicThresh(gray_image,115,True)
    # binary_image = util.convert_gray_to_binary_adaptiveThresh(gray_image,True,True)
    _,saturation_img,_ = util.convert_rgb_to_hsv(rgb_image,True)
    edge_img_saturation = util.canny_edge(saturation_img, 100, 200,True)
    contours = util.get_contours_options(edge_img_saturation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_properties = util.get_contours_info(contours)
    perim_min = 1000
    print "min perimeter is %d" % (perim_min)
    kwargs = {'Perim': perim_min}
    filtered_contours = util.filter_contours_minValue(contours_properties, **kwargs)
    util.draw_contours(rgb_image, binary_image, filtered_contours)
    util.draw_contours_coordinates(binary_image,filtered_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
