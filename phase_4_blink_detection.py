# coding: latin-1

import argparse, pickle, time, mindwave, cv2, numpy as np
from collections import deque
from plotter import Plotter
from sklearn.linear_model import LogisticRegression, LinearRegression

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required model id
parser.add_argument('--model_id', help='Required model id', type=str)

# Optional used buffer size in previous phases
parser.add_argument('--used_buffer_size', help='Optional used buffer size in previous phases', default=35, type=int)

# Parse srguments
args = parser.parse_args()

model_location = './data/model/' + args.model_id

# get_max_diff gets the max difference between the lowest and highest values in the buffer
def get_max_diff(buf):
    return max(buf) - min(buf)

model = pickle.load(open(model_location, 'rb'))

buffer = deque([], args.used_buffer_size)

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')
print("Hold Still...")
time.sleep(1)
print("Wait for it...")
time.sleep(1)
while (headset.poor_signal > 5):
    pass
print("Lets do this!")
plotter = Plotter(500, -500, 500)

# Fill buffer first 
while len(buffer) < buffer.maxlen:
    eeg = headset.raw_value
    plotter.plotdata([eeg])
    buffer.append(eeg)
    time.sleep(.01)

blinking_counter = 0
blinking = False
while True:
    if model.predict(np.array(buffer).reshape(1, -1)):
        if not blinking:
            print(buffer)
            print("BLINK: " + str(blinking_counter))
            blinking = True
            blinking_counter += 1
    else:
        blinking = False

    eeg = headset.raw_value
    plotter.plotdata([eeg])
    buffer.append(eeg)
    time.sleep(.01)

    # Check for exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Exiting...')
        break

headset.stop()
