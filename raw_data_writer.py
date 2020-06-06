#coding: latin-1

import threading, sys, select, time, datetime, math

def startFileWriter(headset, collector_max_seconds, eeg_location, is_video_ready):
  try:
    eeg_data_file = open(eeg_location + '.csv', 'w')

    is_video_ready.acquire()
    is_video_ready.wait()

    finish_time_in_millis = collector_max_seconds * 1000 + int(time.time() * 1000)
      
    while int(time.time() * 1000) < finish_time_in_millis:

      eeg = headset.raw_value

      data_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S.%f')
      eeg_data_file.write(str(data_time) + ',' + str(eeg) + '\n')

      time.sleep(.01)
  finally:
    eeg_data_file.close()