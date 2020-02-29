# coding: latin-1
import argparse
import csv
import os
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

print('reading training data...')

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required .dat file location argument
parser.add_argument('--dir', help='Input directory with data for model')
parser.add_argument('--model', help='Output path for AI model')

# Parse arguments
args = parser.parse_args()

training_dataset = []
training_dataset_result = []
training_row = []

# ver de saltear los ptimeros 20
# fecha, valor, veracidad
for filename in os.listdir(args.dir):
    with open(str(args.dir) + "/" + str(filename)) as inputfile:
        reading_true = False
        training_row = []
        for row in csv.reader(inputfile):
            value = int(row[1])
            is_blink = row[2] == 'True'
            if (not reading_true and not is_blink) or (reading_true and is_blink):
                training_row.append(value)
                if len(training_row) == 50:
                    training_dataset.append(training_row)
                    training_dataset_result.append(reading_true)
                    reading_true = not reading_true
                    training_row = []
            else:  # not reading true && is blink || reading true && not blink
                training_row = []

if len(training_dataset_result) % 2 != 0:
    training_dataset.pop()
    training_dataset_result.pop()

trainedLogisticRegression = LogisticRegression(random_state=0, solver='liblinear')
trainedLogisticRegression.fit(training_dataset, training_dataset_result)

pickle.dump(trainedLogisticRegression, open(args.model, 'wb'))
