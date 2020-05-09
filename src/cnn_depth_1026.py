#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:16:22 2020

@author: ivan
"""
#bilo je python3

#PART 1 - BUILDING A CNN
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

#Initializing the CNN
classifier = Sequential() #kreiramo objekt klase Sequential 

#1 sloj. konvolucija
classifier.add(Conv2D(32,(3,3),input_shape = (64,64,3), activation ='relu'))
#32 - broj filtera, 3x3 dimanzije filtera
#kolko ima feature detectora, tolko ima i feature mapa
# input shape - expected format input image, kasnije cemo ih skalirati na tu veličinu



#2. sloj - pooling 
classifier.add(MaxPooling2D(pool_size = (2,2)))
#uglavnom je 2*2


#jos jedan sloj da dobimo vecu acc
 #sve isto samo nema vise input shape
classifier.add(Conv2D(32,(3,3), activation ='relu')) #sve isto samo nema vise input shape, mogla bi staviti 64
classifier.add(MaxPooling2D(pool_size = (2,2)))

#3.sloj - flatten 
classifier.add(Flatten())

#4. korak fully connected layer , samo cemo hidden i output
classifier.add(Dense(units = 128, kernel_initializer = 'uniform', activation = 'relu'))
#128 - kolko ih ima u skrivenom, eksperimantalno, ni premalo ni previse, oko 100 je oke, uzimamo potenciju 2
classifier.add(Dense(units = 5, kernel_initializer = 'uniform', activation = 'softmax')) 
#da je binarno- sigmoid  #pazi, promijeni ovjde unit s obzirom na to kolko imas klasa

#compile 
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
#da je binary outcome bila bi binary_crossentropy

## kopirano sa https://keras.io/preprocessing/image/
#image augumenttaion, ujedno i fitting i testing

from keras.preprocessing.image import ImageDataGenerator

#image augumentation part
train_datagen = ImageDataGenerator(rescale=1./255,    #tu je ovaj rescale, slicno ko feature scaling prije, sve vrijdnosti pixea ce biti [0,1]
                                   shear_range=0.2, #shearing - smicanje, transvection
                                   zoom_range=0.2, #random zoom na sliku
                                   horizontal_flip=True) #postoji jos svasta, i vertical flip, pogledaj dokumntaciju

test_datagen = ImageDataGenerator(rescale=1./255) #ovo ce samo napraviti za test


training_set = train_datagen.flow_from_directory(        #napraviti ce cijeli train_Set
        'marsela_dataset/1026_1/1026/dataset2/training_set',                          #ovo tu treba promijeniti, odkud cemo uzet slike, ne treb cijeli path jer je dataset u working direcotry
        target_size=(64, 64),                            #i ovo, bilo je 150, velicina slike koju ocekujes u cnn modelu , a gore smo napisali da zelimo 64x64
        batch_size=32,                                  #broj slika nakon kojih ce tezine biti updatane, a sadrze te izoblicene slike
        class_mode='categorical')    #dvije klase binary

test_set = test_datagen.flow_from_directory('marsela_dataset/1026_1/1026/dataset2/test_set',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='categorical')

 #treniranje i testiranje 
classifier.fit_generator(training_set,
                         steps_per_epoch=1235, #broj slika koje imamo u training setu
                         epochs=25,
                         validation_data=test_set,
                         validation_steps=140) #broj slika u test setu 

classifier.save("model2_1026.h5")

#### prediction 
from keras.models import load_model 
from keras.preprocessing import image
import numpy as np

#classifier = load_model('model_1026.h5')
test_image = image.load_img("predict/-0.002/-0.002_frame_828.jpg", target_size = (64,64)) #mora biti iste velicine ko train. uzela iz 0.002
#sad je size (64,64), 2D , treba bi 64x64x3
test_image = image.img_to_array(test_image)  #sad je 3D


#classifier.predict(test_image) #ovo ne bude proslo, trazi 4tu dimenziju, tj batch. 
#predict prima inpute samo u batchu. ovo bude batch koji ima jednu sliku

test_image = np.expand_dims(test_image, axis = 0) #axis je pozicija indexa u dimanziji, axis = 0 znaci da dodajemo prvi index, a ic ce na prvo mjesto jer tako  trazi predict
#sad je (1,64,64,3)
result  =classifier.predict(test_image) #dobim array [0,0,0,0,1]
#korisiti atribut class_indicies da vidis kak je to mapirano
indexi_klasa  = training_set.class_indices
# dobim disctionary {'-0.0005': 1, '-0.0015': 3, '-0.0': 0, '-0.001': 2, '-0.002': 4}
 

result_list = result.tolist()
result_list = result_list[0]
prediction_index = result_list.index(1.0)
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

print (prediction)


