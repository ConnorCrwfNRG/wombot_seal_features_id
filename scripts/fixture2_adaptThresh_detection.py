#!/usr/bin/env python

import numpy as np
import cv2
import sys
import util

def main():
    image_name = "../images/test_fixture2_sec1.jpg"
    # image_name = "../images/fixture1_saturation.png"
    rgb_image = util.read_starting_image(image_name, False)
    height, width, _ = util.get_image_size(rgb_image)
    gray_image= util.convert_rgb_to_gray(rgb_image,False)
    binary_image = util.convert_gray_to_binary_adaptiveThresh(gray_image, True, False)
    contours = util.get_contours(binary_image)
    #gets properties of all the contours found from above
    contours_properties = util.get_contours_info(contours)
    #criteria to filter out
    # y_pos_min = int(height*0.29)
    y_pos_min = 700
    # area_min = int(height*width*0.03)
    area_min = 20000
    print "min y position is %d, and min area is %d " % (y_pos_min, area_min)
    kwargs = {'Y_Pos_Ctr': y_pos_min, 'Area': area_min}
    filtered_properties = util.filter_contours_minValue(contours_properties, **kwargs)
    #or the below also works even though the keys arn't specified as strings; pretty cool.
    # filtered_properties = util.filter_contours_minValue(contours_properties, Y_Pos_Ctr=y_pos_min, Area=area_min)
    util.draw_contours(rgb_image, binary_image, filtered_properties)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
