# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:05:33 2020

@author: ivan
"""


import pickle
import csv
import cv2



p = 0 #samo da napise header i poslije je brojac
n = 1389 #kolko ima ukupno .txt filova


path1 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/yaw_depth/yaw_depth_'
#path2 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/optoforce/z_force_'

#slike
path3 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/frames/frame_'


for i in range(1,n+1):
    with open(path1+str(i)+'.txt','rb') as f1:
                procitana_lista1 = pickle.load(f1)
                depth = procitana_lista1[1]
                flag = procitana_lista1[2]
                frame = cv2.imread(path3+str(i)+'.jpg')
                if flag == 1: 
                 cv2.imwrite('/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/cnn_dataset/'+str(depth)+'/'+str(depth)+'_frame_'+str(i)+'.jpg', frame)
              
               
        
    f1.close()
   


