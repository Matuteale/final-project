# coding: latin-1

import argparse, csv, os, pickle, numpy as np, matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from collections import deque

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required model name
parser.add_argument('--model_name', help='Required model name', type=str)

# Required id of the training data
parser.add_argument('--id', help='Required id of the training data', type=str)

# Parse arguments
args = parser.parse_args()

training_data_location = './data/training_data/' + args.id + '.csv'
model_location = './data/model/' + args.model_name

model = pickle.load(open(model_location, 'rb'))

input = np.array([])
output = []

with open(training_data_location) as training_data_file:
    for line in csv.reader(training_data_file):
        input = np.append(input, model.predict_proba([int(line[1])])[:, 1][0])
        output.append(1 if bool(line[2]) else 0)

fpr, tpr, _ = roc_curve(output, input)

plt.figure()
# Adding the ROC
plt.plot(fpr, tpr, color='red',
lw=2, label='ROC curve')
# Random FPR and TPR
plt.plot([0, 1], [0, 1], color='blue', lw=2, linestyle='--')
# Title and label
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC curve')
plt.show()