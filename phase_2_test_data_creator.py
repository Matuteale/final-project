#coding: latin-1

import thread

from video_writer import startVideoRecording
import time, datetime
from raw_data_writer import startFileWriter
import argparse
import csv
import cv2

class DataPoint:
  def __init__(self, time, raw):
    self.time = time
    self.raw = int(raw)

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required .dat file location argument
parser.add_argument('--video', help='A required file with the video')
parser.add_argument('--data', help='A required file with the data')

# Parse srguments
args = parser.parse_args()


cap = cv2.VideoCapture(args.video)
print(cap.get(cv2.CAP_PROP_POS_MSEC))
# print(datetime.datetime.strptime(firstTime, '%Y-%m-%d-%H-%M-%S.%f'))
# caca = datetime.datetime.strptime(firstTime, '%Y-%m-%d-%H-%M-%S.%f')
# print(caca)
# exit(0)
blink_times = []
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(40) & 0xFF == ord('b'):
            print('blink saved')
            blink_times.append(cap.get(cv2.CAP_PROP_POS_MSEC))

    # Break the loop
    else:
        break

print(blink_times)

# levantar los archivos como variables.
lines = []
with open(args.data) as inputfile:
    for row in csv.reader(inputfile):
        dp = DataPoint(row[0], row[1])
        lines.append(dp)
inputfile.close()

firstTime = lines[0].time
firstTime = datetime.datetime.strptime(firstTime, '%Y-%m-%d-%H-%M-%S.%f')
secondTime = lines[1].time
secondTime = datetime.datetime.strptime(secondTime, '%Y-%m-%d-%H-%M-%S.%f')
# print(dt.time())

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


startMs = unix_time_millis(firstTime)

counter = 0
nextMs = blink_times.pop(0)
true_indexes = []
for line in lines:
    thisMs = unix_time_millis(datetime.datetime.strptime(line.time, '%Y-%m-%d-%H-%M-%S.%f')) - startMs
    if nextMs < thisMs: # modificar los 10 anteriores
        true_indexes.append(counter-10)
        if len(blink_times) == 0:
            break
        nextMs = blink_times.pop(0)
    counter += 1

print(true_indexes)

file = open('data/processed/test.csv', 'w')
counter = 0
next_counter = true_indexes.pop(0)

while counter < len(lines):
    if counter >= next_counter:
        counterTwo = 50
        while counterTwo > 0:
            file.write(lines[counter].time + ',' + str(lines[counter].raw) + ',True\n')
            counterTwo -= 1
            counter += 1
        if len(true_indexes) != 0:
            next_counter = true_indexes.pop(0)
        else:
            next_counter = 999999999
    else:
        file.write(lines[counter].time + ',' + str(lines[counter].raw) + ',False\n')
        counter += 1

# luego generar un for externo que abra un frame, luego internamente en otro for iterar por los registros hasta llegar al
# tiempo que corresponde al siguiente frame. salir y pasar de frame en el externo. Repetir
# Escuchar por la tecla espacio. cuando se clickea, agregar un 1 a los registros hasta el siguiente frame
# startVideoRecording(start_time, './data/raw/videos/' + args.file_id, video_ready, collector_max_seconds, notify_finish)

