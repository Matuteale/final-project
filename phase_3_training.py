# coding: latin-1
import csv
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

print('reading training data...')
training_dataset = []
training_dataset_result = []
training_row = []
currentState = 'lookingForFalse'

# ver de saltear los ptimeros 20
# fecha, valor, veracidad
with open('data/raw/training_data_v2.csv') as inputfile:
    reading_true = False
    for row in csv.reader(inputfile):
        value = int(row[1])
        is_blink = row[2] == 'True'
        if (not reading_true and not is_blink) or (reading_true and is_blink):
            training_row.append(value)
            if len(training_row) == 10:
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

pickle.dump(trainedLogisticRegression, open('data/lrModel', 'wb'))

test = pickle.load(open('data/lrModel', 'rb'))

print (test)
print(test.predict(np.array([1000,1050,1500,1050,1050,1050,1050,1050,1500,1000]).reshape(1,-1)))