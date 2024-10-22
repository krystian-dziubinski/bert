import sys
import cv2
import numpy as np
import time


def find_depth(right_point, left_point, frame_right, frame_left):


    frame_rate = 30    #Camera frame rate (maximum at 120 fps)
    B = 9.5            #Distance between the cameras [cm]
    f = 4              #Camera lense's focal length [mm]
    alpha = 60         #Camera field of view in the horisontal plane [degrees]

    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)

    else:
        print('Left and right camera frames do not have the same pixel width')

    x_right = right_point[0]
    x_left = left_point[0]

    # CALCULATE THE DISPARITY:
    disparity = x_left-x_right      #Displacement between left and right frames [pixels]

    # CALCULATE DEPTH z:
    zDepth = (B*f_pixel)/disparity             #Depth in [cm]

    return zDepth

