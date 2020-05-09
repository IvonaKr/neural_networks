Skripte :

`avi_to_jpg.py`

`labels2.py`

`cnn_dataset.py`

`cnn_dataset_train_test.py`

su korištene kako bi se dataset u `pickle` formatu obradio u oblik prihvatljiv za treniranje neuronske mreže.

Model potpuno povezane klasifikacijske konvolucijske mreže za predviđanje dan je u skripti `cnn_depth_1026.py`.
Zavisna varijabla je `depth`, s 5 različitih klasa.

Predikcija modela u stvarnom vremenu omogućena je pomoću dva noda :

`picture_publisher.py`  koji objavljuje  topic čija je poruka tipa `Image`, te topic sa "custom" porukom tipa `CnnFeatures` koji nosi podatak o dubini.

`cnn_predictions.py` koristi istrenirani model za predviđanje dubine na temelju slika dobivenih sa ros mastera u stvarnom vremenu.

### Skidanje paketa
```
mkdir ~/your_ws/src
cd ~/your_ws
catkin init
cd src
git clone https://github.com/IvonaKr/neural_networks.git
cd ..
catkin build
```

### Pokretanje paketa

roslaunch neural_networks cnn_predictions.launch
