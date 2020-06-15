# coding: latin-1

import argparse, csv, os, pickle, numpy as np, matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from collections import deque

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required model name
parser.add_argument('--model_name', help='Required model name', type=str)

# Optional used function to process buffer
parser.add_argument('--used_processing_func', help='Optional used function to process buffer. Options are \'max_diff\' and \'mean\'', default='max_diff', type=str)

# Parse arguments
args = parser.parse_args()

training_data_location = './data/training_data/' + args.used_processing_func + '/'
model_location = './data/model/' + args.model_name

model = pickle.load(open(model_location, 'rb'))

input = np.array([])
output = []
for filename in os.listdir(training_data_location):
    if str(filename).startswith('.'):
        continue
    with open(training_data_location + '/' + str(filename)) as training_data_file:
        for line in csv.reader(training_data_file):
            input = np.append(input, model.predict_proba(np.array([int(line[1])]).reshape(1, -1))[:, 1][0])
            output.append(1 if str(line[2]) == 'True' else 0)

fpr, tpr, _ = roc_curve(output, input)
model_score = roc_auc_score(output, input)

print('Model score: ' + str(model_score))

plt.figure()
plt.plot(fpr, tpr, color='red', lw=2, label='ROC curve')
plt.plot([0, 1], [0, 1], color='blue', lw=2, linestyle='--')
# Title and label
plt.xlabel('False Positive Ratio')
plt.ylabel('True Positive Ratio')
plt.title('ROC Curve (Max Diff Logistic Regression)')
bbox_props = dict(boxstyle='square,pad=0.3', fc='w', ec='k', lw=0.72)
kw = dict(xycoords='data',textcoords="axes fraction", bbox=bbox_props, ha='right', va='top')
area_under_curve = 'Area under the curve = {:.5f}'.format(model_score)
plt.annotate(area_under_curve, xy=(0.5, 0.5), xytext=(0.75, 0.5), **kw)
plt.grid(b=True, which='major', linestyle='-', axis='y')
plt.show()