#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 18:56:45 2020

@author: ivan
"""
import rospy
from sensor_msgs.msg import Image
from neural_networks.msg import CnnFeatures
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import glob
import std_msgs.msg





def picture_publisher():
    pub1 = rospy.Publisher('/cnn_image', Image, queue_size =10)
    pub2 = rospy.Publisher('/cnn_features', CnnFeatures, queue_size = 10)
    rospy.init_node('picture_publisher_node', anonymous = True)
    bridge = CvBridge()
    rate = rospy.Rate(1)


    while not rospy.is_shutdown():

        for filepath in glob.iglob(predict_path):
            pom_path = filepath.split('/')[-2:]
            pom_path[0] = pom_path[0]+'/'
            pom_path = ''.join(pom_path)   # predict/*.jpg


            cnn_features = CnnFeatures()
            image =cv2.imread(filepath)

            depth = []
            pom = pom_path[9:] #da dobim 0.0_frame_731.jpg
            print (pom)
            for i in pom :
                if i.isdigit() or i =='.':
                    depth.append(i)
                elif i =='_':
                    break

            #depth =''.join(depth)
            depth =''.join(depth)
            print(depth)


            #depth = np.float32(depth)
            image = np.uint8(image)
            image_message  = bridge.cv2_to_imgmsg(image, encoding="passthrough" )

            cnn_features.depth = depth

            rospy.loginfo(image)
            rospy.loginfo(cnn_features)

            pub1.publish(image_message)
            pub2.publish(cnn_features)
            rate.sleep()





if __name__ == '__main__':
    
    #INIT NODE MORA BITI PRIJE GET PARAM!!!!!
    rospy.init_node('picture_publisher_node', anonymous = True)
    
    #directory = '/home/ivan/catkin2_workspace/src/neural_networks/'
    directory = rospy.get_param('~directory')
    print (directory)
    predict_path =directory +'/src/predict/*.jpg'   
    
    try:
        picture_publisher()
    except rospy.ROSInterruptException:
        pass
