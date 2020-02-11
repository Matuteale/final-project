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

# levantar los archivos como variables.
lines = []
print (args)
with open(args.data) as inputfile:
    for row in csv.reader(inputfile):
        dp = DataPoint(row[0], row[1])
        lines.append(dp)
inputfile.close()

firstTime = lines[0].time
milliPerFrame = 1000.0/29.0
# prepararse para iterrar renglon por renglon en data y frame por frame del video cv2
cap = cv2.VideoCapture(args.video)
print(datetime.datetime.strptime(firstTime, '%Y-%m-%d-%H-%M-%S.%f'))
caca = datetime.datetime.strptime(firstTime, '%Y-%m-%d-%H-%M-%S.%f')
print(caca.)
exit(0)
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        #iterrar x veces
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(9) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# luego generar un for externo que abra un frame, luego internamente en otro for iterar por los registros hasta llegar al

# tiempo que corresponde al siguiente frame. salir y pasar de frame en el externo. Repetir

# Escuchar por la tecla espacio. cuando se clickea, agregar un 1 a los registros hasta el siguiente frame

# startVideoRecording(start_time, './data/raw/videos/' + args.file_id, video_ready, collector_max_seconds, notify_finish)

