# -*- coding: utf-8 -*-
import fasttext

INPUT_TXT = './../R/data_ft_test.txt'
OUTPUT_PATH_SKIPGRAM = './skip_model'
OUTPUT_PATH_CBOW = './cbow_model'

lr=0.02
dim=300
ws=5
epoch=1
min_count=1
neg=5
loss='ns'
bucket=200000
minn=3
maxn=6
thread=4
t=1e-4
lr_update_rate=100

# Learn the word representation using skipgram model
skipgram = fasttext.skipgram(INPUT_TXT, OUTPUT_PATH_SKIPGRAM, lr=lr, dim=dim, ws=ws, epoch=epoch,
	min_count=min_count, neg=neg, loss='ns', bucket=bucket, minn=minn, maxn=maxn, thread=thread,
	t=t, lr_update_rate=lr_update_rate)

# Get the vector of some word
print skipgram['3']
print("SKP FIN")

# Learn the word representation using cbow model
cbow = fasttext.cbow(INPUT_TXT, OUTPUT_PATH_CBOW, lr=lr, dim=dim, ws=ws, epoch=epoch, 
        min_count=min_count, neg=neg, loss='ns', bucket=bucket, minn=minn, maxn=maxn, thread=thread, 
        t=t, lr_update_rate=lr_update_rate)

# Get the vector of some word
print cbow['3']
print("CBW FIN")

# Load pre-trained skipgram model
SKIPGRAM_BIN = OUTPUT_PATH_SKIPGRAM + '.bin'
skipgram = fasttext.load_model(SKIPGRAM_BIN)
print skipgram['3']

# Load pre-trained cbow model
CBOW_BIN = OUTPUT_PATH_CBOW + '.bin'
cbow = fasttext.load_model(CBOW_BIN)
print cbow['3']
