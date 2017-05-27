# -*- coding: utf-8 -*-
import fasttext as ft
import os

# on test/ and move to the example directory
current_dir = os.path.dirname(__file__)
input_file = os.path.join(current_dir, './../R/data_ft.txt')
check_file = './../R/data_ft_.txt'
output = './model'
test_file = './../R/data_ft_test.txt' # with label
SET_TRAIN_OR_LOAD = 'TRAIN'
#SET_TRAIN_OR_LOAD = 'LOAD'

# set params
dim=5
lr=0.02
epoch=1
ws=10
min_count=1
word_ngrams=5
bucket=200000
thread=4
silent=1
loss='ns'
neg=10
minn=1
maxn=5

label_prefix='__label__'
classifier = ''

if 'TRAIN' == SET_TRAIN_OR_LOAD:
	# Train the classifier
	classifier = ft.supervised(input_file, output, dim=dim, lr=lr, epoch=epoch, ws=ws,
		min_count=min_count, word_ngrams=word_ngrams, bucket=bucket, loss=loss, neg=neg,
		thread=thread, silent=silent, minn=minn, maxn=maxn, label_prefix=label_prefix)

	# Test the classifier
	result = classifier.test(input_file)
	print 'P@1:', result.precision
	print 'R@1:', result.recall
	print 'Number of examples:', result.nexamples
else:
	classifier = ft.load_model(output+'.bin')

# Predict some text
f = open(test_file)
lines2 = f.readlines()
f.close()

all_count = 0
count1 = 0
count2 = 0

for index,line in enumerate(lines2):
	texts = [line]
	#print texts
	labels = classifier.predict(texts, k=1)
	#print labels[0][0]
	if index <= 100:
		if 'TRAIN' == SET_TRAIN_OR_LOAD:
			if '1' == labels[0][0]:
				count1 = count1 + 1
			if '__label__1' == labels[0][0]:
				count1 = count1 + 1
	else:
		if 'TRAIN' == SET_TRAIN_OR_LOAD:
			if '2' == labels[0][0]:
				count2 = count2 + 1
			if '__label__2' == labels[0][0]:
				count2 = count2 + 1
	all_count = all_count + 1
	# Or with the probability
	#labels = classifier.predict_proba(texts, k=1)
	#print labels

print 'NP:\t\t', count1
print 'TP:\t\t', count2
print 'All:\t\t', all_count
print 'recall:\t\t', (float)(count1)/(float)(100)
print 'precision:\t', (float)(count1)/(float)(count1+(9900-count2))
print 'accuray:\t',(float)(count1+count2)/(float)(all_count)
print ''
print 'recall:\t\t', (float)(count2)/(float)(9900)
print 'precision:\t', (float)(count2)/(float)(count2+(100-count1))
print 'accuray:\t',(float)(count1+count2)/(float)(all_count)
