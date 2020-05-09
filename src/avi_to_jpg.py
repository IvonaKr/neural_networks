#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import cv2
 


for i in range(1,1390):
    cap = cv2.VideoCapture('/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/video/video_'+str(i)+'.avi')
    ret, frame = cap.read()
    
    cv2.imwrite('frame_'+str(i)+'.jpg', frame)


cv2.waitKey(0)
cv2.destroyAllWindows()






