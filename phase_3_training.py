# coding: latin-1

import argparse, csv, os, pickle, numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required id for the model
parser.add_argument('--id', help='Required id for the model', type=str)

# Optional model type
parser.add_argument('--model_type', help='Optional model type', default='logistical_regression', type=str)

# Optional used buffer size in previous phases
parser.add_argument('--used_buffer_size', help='Optional used buffer size in previous phases', default=35, type=int)

# Parse arguments
args = parser.parse_args()

training_data_location = './data/training_data/'
model_location = './data/model/' + args.id + '_' + args.model_type

training_dataset = []
training_dataset_result = []

for filename in os.listdir(training_data_location):
    with open(training_data_location + '/' + str(filename)) as training_data_file:
        reading_true = False
        training_line = []
        false_jump = 0
        for line in csv.reader(training_data_file):
            value = int(line[1])
            is_blink = str(line[2]) == 'True'
            if (not reading_true and not is_blink and false_jump <= 0) or (reading_true and is_blink):
                training_line.append(value)
                if len(training_line) == args.used_buffer_size * 2:
                    for item in training_line:
                        training_dataset.append([item])
                        training_dataset_result.append(reading_true)
                    reading_true = not reading_true
                    training_line = []
                    if not reading_true:
                        false_jump = args.used_buffer_size
            else:  # not reading true && is blink || reading true && not blink
                training_line = []
                if not is_blink:
                    false_jump -= 1

if len(training_dataset_result) % 2 != 0:
    training_dataset.pop()
    training_dataset_result.pop()

# Train and save the model
trained_model = None
print(args.model_type)
if args.model_type == 'logistical_regression':
    trained_model = LogisticRegression(random_state=0, solver='liblinear')
    print(trained_model)
else:
    trained_model = LinearRegression(random_state=0, solver='liblinear')

trained_model.fit(training_dataset, training_dataset_result)
pickle.dump(trained_model, open(model_location, 'wb'))
