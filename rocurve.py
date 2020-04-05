import argparse
import csv
import os
import pickle
from random import random

import numpy as np
from collections import deque

from sklearn.metrics import roc_curve

parser = argparse.ArgumentParser()

# Required .dat file location argument
parser.add_argument('--file', help='Input directory with data for model')
parser.add_argument('--model', help='Output path for AI model')

# Parse arguments
args = parser.parse_args()

roc_input = []
training_dataset_result = []
training_row = []
model = pickle.load(open(args.model, 'rb'))
buffer = deque([], 50)
input = np.array([])
output = []
buffer2 = deque([], 50)

with open(str(args.file)) as inputfile:
    for row in csv.reader(inputfile):
        if len(buffer) < buffer.maxlen:
            buffer.append(int(row[1]))
            buffer2.append(row[2])
            continue
        counter = 0
        for i in buffer2:
            if i == 'True':
                counter += 1

        input = np.append(input, (random() * 0.5 + 0.5 if model.predict(np.array(buffer).reshape(1, -1)) == 1 else random() * 0.5))
        output.append(1 if counter > 20 else 0)
        buffer.append(int(row[1]))
        buffer2.append(row[2])

fpr, tpr,_=roc_curve(output,input, pos_label=1)

import matplotlib.pyplot as plt
plt.figure()
##Adding the ROC
plt.plot(fpr, tpr, color='red',
 lw=2, label='ROC curve')
##Random FPR and TPR
plt.plot([0, 1], [0, 1], color='blue', lw=2, linestyle='--')
##Title and label
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC curve')
plt.show()