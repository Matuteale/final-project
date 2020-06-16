# coding: latin-1

import argparse, csv, os, pickle, numpy as np
from sklearn import linear_model
# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required id for the model
parser.add_argument('--id', help='Required id for the model', type=str)

# Optional used buffer size in previous phases
parser.add_argument('--used_buffer_size', help='Optional used buffer size in previous phases', default=35, type=int)

# Optional used function to process buffer
parser.add_argument('--used_processing_func', help='Optional used function to process buffer. Options are \'max_diff\' and \'mean\'', default='max_diff', type=str)

# Parse arguments
args = parser.parse_args()

training_data_location = './data/training_data/' + args.used_processing_func + '_buff_' + str(args.used_buffer_size) + '/'
model_location = './data/model/' + args.id

training_dataset = []
training_dataset_result = []

for filename in os.listdir(training_data_location):
    if str(filename).startswith('.'):
        continue
    with open(training_data_location + str(filename)) as training_data_file:
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
                        false_jump = args.used_buffer_size * 2
            else:  # not reading true && is blink || reading true && not blink
                training_line = []
                if not is_blink:
                    false_jump -= 1

if len(training_dataset_result) % 2 != 0:
    training_dataset.pop()
    training_dataset_result.pop()

# Train and save the model
trained_model = linear_model.LogisticRegression(random_state=0, solver='liblinear')
trained_model.fit(training_dataset, training_dataset_result)
pickle.dump(trained_model, open(model_location, 'wb'))
