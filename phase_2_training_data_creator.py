# coding: latin-1

import datetime, cv2, argparse, csv
from collections import deque
from data_point import DataPoint

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# A required id to use along all the phases
parser.add_argument('--id', help='A required id to use along all the phases', type=str)

# Optional buffer size to group egg raw data
parser.add_argument('--buffer_size', help='Optional buffer size to group egg raw data', default=35, type=int)

# Optional function to process buffer
parser.add_argument('--processing_func', help='Optional function to process buffer. Options are \'max_diff\' and \'mean\'', default='max_diff', type=str)

# Parse arguments
args = parser.parse_args()

# epoch time
epoch = datetime.datetime.utcfromtimestamp(0)

video_location = './data/video/' + args.id + '.avi'
eeg_location = './data/eeg/' + args.id + '.csv'
training_data_location = './data/training_data/' + args.processing_func + args.id

# get_max_diff gets the max difference between the lowest and highest values in the buffer
def get_max_diff(buf):
    return max(buf) - min(buf)

# unix_time_millis
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

# Show video and record blink times by hand
blink_times_in_millis = []
cap = cv2.VideoCapture(video_location)
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(60) & 0xFF == ord('b'):
            print('Blink saved')
            blink_times_in_millis.append(cap.get(cv2.CAP_PROP_POS_MSEC))
    else:
        break

# levantar los archivos como variables.
eeg_lines = []
with open(eeg_location) as eeg_file:
    for line in csv.reader(eeg_file):
        dp = DataPoint(line[0], line[1])
        eeg_lines.append(dp)
eeg_file.close()

start_time_in_millis = unix_time_millis(datetime.datetime.strptime(eeg_lines[0].time, '%Y-%m-%d-%H-%M-%S.%f'))

next_blink_time_in_millis = blink_times_in_millis.pop(0)
true_indexes = []
counter = 0

for line in eeg_lines:
    eeg_time_in_millis = unix_time_millis(datetime.datetime.strptime(line.time, '%Y-%m-%d-%H-%M-%S.%f')) - start_time_in_millis
    if next_blink_time_in_millis < eeg_time_in_millis:
        true_indexes.append(counter - args.buffer_size)
        if len(blink_times_in_millis) == 0:
            break
        next_blink_time_in_millis = blink_times_in_millis.pop(0)
    counter += 1

training_data_file = open(training_data_location + '.csv', 'w')

buffer = deque([], args.buffer_size)
next_true_index = true_indexes.pop(0)
counter = 0

while counter < len(eeg_lines):
    if len(buffer) < buffer.maxlen:
        buffer.append(eeg_lines[counter].raw)
        continue
    if counter >= next_true_index:
        counter_two = args.buffer_size * 2
        while counter_two > 0:
            training_data_file.write(eeg_lines[counter].time + ',' + str(get_max_diff(buffer)) + ',True\n')
            counter_two -= 1
            counter += 1
            if counter == len(eeg_lines):
                break
            buffer.append(eeg_lines[counter].raw)
        if len(true_indexes) != 0:
            next_true_index = true_indexes.pop(0)
        else:
            next_true_index = 9999999999
    else:
        training_data_file.write(eeg_lines[counter].time + ',' + str(get_max_diff(buffer)) + ',False\n')
        counter += 1
        if counter < len(eeg_lines):
            buffer.append(eeg_lines[counter].raw)
