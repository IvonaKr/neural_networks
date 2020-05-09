# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:05:33 2020

@author: ivan
"""


import pickle
import csv



p = 0 #samo da napise header i poslije je brojac
n = 1389 #kolko ima ukupno .txt filova
#path1 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/yaw_depth/yaw_depth_1.txt'
#path2 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/optoforce/z_force_100.txt'

path1 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/yaw_depth/yaw_depth_'
path2 = '/home/ivan/catkin_workspace/src/diplomski/scripts/marsela_dataset/1026_1/1026/optoforce/z_force_'


with open('labels.csv', 'wb') as csvfile :
    filewriter = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    for i in range(1,n+1):
        with open(path1+str(i)+'.txt','rb') as f1, open (path2+str(i)+'.txt', 'rb') as f2:
                    procitana_lista1 = pickle.load(f1)
                    procitana_lista2 = pickle.load(f2)

                    yaw = procitana_lista1[0]
                    depth = procitana_lista1[1]
                    flag = procitana_lista1[2]
                    force = procitana_lista2[0]
                    if not(p) :
                        filewriter.writerow(['jaw', 'depth', 'force'])
                        p = 1
                    if flag == 1: #ima ih par sa -1. na kraju ih bude 1376
                        filewriter.writerow([yaw , depth, force])
        f1.close()
        f2.close()
csvfile.close()

#ne znam zakaj al mora biti puni put
