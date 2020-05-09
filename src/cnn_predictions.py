#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:09:56 2020

@author: ivan
"""

import rospy
import std_msgs.msg
from neural_networks.msg import CnnFeatures
from sensor_msgs.msg import Image
import message_filters
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2
from keras.models import load_model
#from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
#treba mi za kasnije da znam class_indicies

bridge = CvBridge()

def callback(cnn_image,cnn_feature):
    global bridge
    print('dobila poruke')

    try:
        cv_image = bridge.imgmsg_to_cv2(cnn_image, "8UC3") #al 480x640x3, al mi treba 64x64x3
        dim = (64,64)
        cv_image = cv2.resize(cv_image,dim) #super 64,64,3
        #print(cv_image.shape)
        test_image = np.expand_dims(cv_image, axis = 0)  #(1x64x64x3)

        result = classifier.predict(test_image)  #dobim array [0,0,0,0,1]
        indexi_klasa  = training_set.class_indices
         # dobim disctionary {'-0.0005': 1, '-0.0015': 3, '-0.0': 0, '-0.001': 2, '-0.002': 4}

        result_list = result.tolist()
        result_list = result_list[0]
        prediction_index = result_list.index(1.0)  #trazim index tamo gdi je 1.0
        if prediction_index == 0:
            prediction = 0.0
        elif prediction_index == 1:
            prediction = 0.0005
        elif prediction_index == 2:
            prediction = 0.001
        elif prediction_index == 3:
            prediction = 0.0015
        elif prediction_index ==4:
            prediction = 0.002
        else:
            prediction = 'error'
        print
        print
        print ('True result : %s, prediction: %s' %(cnn_feature.depth, str(prediction)))
        #print(prediction)
    except CvBridgeError as e :
            print(e)



def listener():


    #da jedan callback obraduje dva topica koristim message_filters
    #image_sub = rospy.Subscriber('cnn_frame', Image, callback)

    image_sub = message_filters.Subscriber('/cnn_image', Image)
    feature_sub = message_filters.Subscriber('/cnn_features', CnnFeatures)

    ts = message_filters.TimeSynchronizer([image_sub, feature_sub],queue_size =10)
    ts.registerCallback(callback)
    rospy.spin()




if __name__ =='__main__':
    rospy.init_node('listener', anonymous=True)

    directory = '/home/ivan/catkin2_workspace/src/neural_networks/'

    #directory = rospy.get_param('~directory')
    print (directory)


    train_datagen = ImageDataGenerator(rescale=1./255,    #tu je ovaj rescale, slicno ko feature scaling prije, sve vrijdnosti pixea ce biti [0,1]
                                       shear_range=0.2, #shearing - smicanje, transvection
                                       zoom_range=0.2, #random zoom na sliku
                                       horizontal_flip=True)
    training_set = train_datagen.flow_from_directory(        #napraviti ce cijeli train_Set
            directory+'/src/marsela_dataset/1026_1/1026/dataset2/training_set',                          #ovo tu treba promijeniti, odkud cemo uzet slike, ne treb cijeli path jer je dataset u working direcotry
            target_size=(64, 64),                            #i ovo, bilo je 150, velicina slike koju ocekujes u cnn modelu , a gore smo napisali da zelimo 64x64
            batch_size=32,                                  #broj slika nakon kojih ce tezine biti updatane, a sadrze te izoblicene slike
            class_mode='categorical')

    classifier = load_model(directory+'/src/model2_1026.h5')


    listener()
