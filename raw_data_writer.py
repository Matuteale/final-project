#coding: latin-1

import threading
import sys, select
import thread
import time, datetime
import math

def startFileWriter(headset, start_time, file_id, video_ready, collector_max_seconds, notify_finish):
  try:

    amount_of_reads = int(collector_max_seconds / 0.01)

    filename = './data/raw/eeg/data_' + file_id + '_' + start_time + '.csv'
    f = open(filename, 'w')

    video_ready.acquire()
    video_ready.wait()

    max_millis = collector_max_seconds * 1000
    start_writing_time = int(time.time() * 1000)
      
    while int(time.time() * 1000) < start_writing_time + max_millis :

      (count, eeg) = (headset.count, headset.raw_value)

      data_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S.%f')
      f.write(str(data_time) + ',' + str(eeg) + '\n')

      time.sleep(.01)
  finally:
    f.close()