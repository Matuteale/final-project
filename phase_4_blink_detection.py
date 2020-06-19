# coding: latin-1

import argparse, pickle, time, cv2, numpy as np
from collections import deque
from plotter import Plotter
from sklearn.linear_model import LogisticRegression, LinearRegression
from NeuroSkyPy.NeuroSkyPy import NeuroSkyPy

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required model id
parser.add_argument('--model_id', help='Required model id', type=str)

# Optional used buffer size in previous phases
parser.add_argument('--used_buffer_size', help='Optional used buffer size in previous phases', default=35, type=int)

# Optional used function to process buffer
parser.add_argument('--used_processing_func', help='Optional used function to process buffer. Options are \'max_diff\' and \'mean\'', default='max_diff', type=str)

# Parse srguments
args = parser.parse_args()

model_location = './data/model/' + args.model_id

# get_max_diff gets the max difference between the lowest and highest values in the buffer
def get_max_diff(buff):
    if len(buff) == 1:
        return np.absolute(buff[0])
    return max(buff) - min(buff)

# get_mean gets the mean of values in the buffer
def get_mean(buff):
    return np.mean(np.absolute(buff))

# apply_processing_func applies the corresponding processing func
def apply_processing_func(buff):
    if args.used_processing_func == 'max_diff':
        return get_max_diff(buff)
    elif args.used_processing_func == 'mean':
        return get_mean(buff)


model = pickle.load(open(model_location, 'rb'))

buffer = deque([], int(args.used_buffer_size/10))

headset = NeuroSkyPy('/dev/tty.MindWaveMobile-DevA') 
headset.start()
print('Hold Still...')
time.sleep(1)
print('Wait for it...')
time.sleep(1)
while (headset.poorSignal > 5):
    pass
print('Lets do this!')
plotter = Plotter(1000, -1000, 1000)

# Fill buffer first 
while len(buffer) < buffer.maxlen:
    eeg = headset.rawValue
    plotter.plotdata([eeg])
    buffer.append(eeg)
    time.sleep(.01)

blinking_counter = 0
blinking = False
while True:
    if model.predict(np.array([apply_processing_func(buffer)]).reshape(1, -1))[0]:
        if not blinking:
            blinking = True
            blinking_counter += 1
            print(buffer)
            print('BLINK: ' + str(blinking_counter))
    else:
        blinking = False

    eeg = headset.rawValue
    plotter.plotdata([eeg])
    buffer.append(eeg)
    time.sleep(.01)

headset.stop()
