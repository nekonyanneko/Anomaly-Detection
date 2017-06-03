# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from numpy import *
from sklearn.preprocessing import MinMaxScaler

length_of_sequences = 50 # 入力データの次元
in_out_neurons = 50 # 出力データの次元
TRAIN_PATH = './../R/data_lstm.txt'
TEST_PATH = './../R/data_lstm_test.txt'
train_data = loadtxt(TRAIN_PATH)
test_data = loadtxt(TEST_PATH)
print 'train_input_data shape: ',train_data.shape
print 'test_input_data shape: ',test_data.shape

#scaler  = MinMaxScaler( feature_range=(0, 1) )
#train_data = scaler.fit_transform(train_data)
#scaler  = MinMaxScaler( feature_range=(0, 1) )
#test_data = scaler.fit_transform(test_data)

X_train = []
y_train = []
X_test = []
y_test = []
X_train = train_data[:,0:length_of_sequences]
y_train = train_data[:,length_of_sequences:length_of_sequences+in_out_neurons]
X_test = test_data[:,0:length_of_sequences]
y_test = test_data[:,length_of_sequences:length_of_sequences+in_out_neurons]

#X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
#X_test  = np.reshape(X_test,  (X_test.shape[0], X_test.shape[1], 1))

print X_train.shape
print y_train.shape
print X_test.shape
print y_test.shape

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.callbacks import EarlyStopping
from keras.models import load_model

#WHICH = 'TRAIN'
WHICH = 'LOAD'
batch_num = 10
epoch = 1000
encoding_dim = 64
model = None

if 'TRAIN' == WHICH:
    model = Sequential()
    model.add(Dense(encoding_dim, batch_input_shape = (None, length_of_sequences), activation='relu'))
    model.add(Dense(length_of_sequences, activation = 'linear'))
    model.compile(loss="mean_squared_error", optimizer="rmsprop")
    early_stopping = EarlyStopping(monitor='val_loss', patience=0, verbose=0, mode='auto')
    #model.fit(X_train, y_train, batch_size=batch_num, nb_epoch=epoch, validation_split=0.02, callbacks=[early_stopping])
    model.fit(X_train, y_train, batch_size=batch_num, nb_epoch=epoch, validation_split=0.1)
    model.summary()
    model.save("model_auto.h5")
else:
    model = load_model('model_auto.h5')

# X_testを入力に次の１つの要素を推測
limit = 0.90
anomaly_num = 50
tn_count = 0
fp_count = 0
fn_count = 0
tp_count = 0

import scipy.spatial.distance
predicted = model.predict(X_test)

#print len(predicted[50]), predicted[50]
#print len(y_test[50]), (y_test[50])

for index in range(0,predicted.shape[0]):
    #print predicted[0]
    #print y_test[0]
    if index == anomaly_num:
        print '***'
    if index < anomaly_num:
        if limit > 1 - scipy.spatial.distance.cosine(predicted[index],y_test[index]):
            print 1 - scipy.spatial.distance.cosine(predicted[index],y_test[index]) , 'TN'
            tn_count = tn_count + 1
        else:
            print 1 - scipy.spatial.distance.cosine(predicted[index],y_test[index]) , 'FP'
            fp_count = fp_count + 1
    else:
        if limit <= 1 - scipy.spatial.distance.cosine(predicted[index],y_test[index]):
            print 1 - scipy.spatial.distance.cosine(predicted[index],y_test[index]) , 'TP'
            tp_count = tp_count + 1
        else:
            print 1 - scipy.spatial.distance.cosine(predicted[index],y_test[index]) , 'FN'
            fn_count = fn_count + 1

print 'TP:', tp_count
print 'FP:', fp_count
print 'TN:', tn_count
print 'FN:', fn_count

print 'accuracy: ', float(tp_count + tn_count)/float(tn_count + tp_count + fp_count + fn_count)
#print 'recall: ', float(tp_count)/float(tp_count + fn_count)
#print 'precision: ', float(tp_count)/float(tp_count + fp_count)
print 'recall: ', float(tn_count)/float(tn_count + fp_count)
print 'precision: ', float(tn_count)/float(tn_count + fn_count)
