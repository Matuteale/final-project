#coding: latin-1

import threading
import sys, select
import thread
import time, datetime

def startFileWriter(headset, start_time, file_id, videoReady):
  try:
    filename = './data/raw/data_' + file_id + '_' + start_time + '.csv'
    f = open(filename, 'w')

    videoReady.acquire()
    videoReady.wait()
      
    while True:
      input = select.select([sys.stdin], [], [], 0)[0]
      if input:
        print('Exiting raw data writer...')
        break
      
      time.sleep(.01)
      (count, eeg) = (headset.count, headset.raw_value)

      data_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S.%f')
      f.write(str(data_time) + ',' + str(eeg) + ',' + '\n')
  finally:
    f.close()