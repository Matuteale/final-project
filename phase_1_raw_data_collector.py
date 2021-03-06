# coding: latin-1

import time, datetime, threading, argparse, _thread
from video_writer import start_video_recording
from raw_data_writer import startFileWriter
from NeuroSkyPy.NeuroSkyPy import NeuroSkyPy

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required id to use along all the phases
parser.add_argument('--id', help='A required id to use along all the phases', type=str)

# Optional max time to run the collector in seconds
parser.add_argument('--max_time', help='Optional max time to run the collector in seconds', default=30, type=int)

# Parse srguments
args = parser.parse_args()

# Threading condition to start both video and data writers
is_video_ready = threading.Condition()

video_location = './data/video/' + args.id
eeg_location = './data/eeg/' + args.id

headset = NeuroSkyPy('/dev/tty.MindWaveMobile-DevA') 
headset.start()

time.sleep(2)

start_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

while (headset.poorSignal > 5):
  print('Headset signal noisy %d. Adjust the headset to adjust better to your forehead.' % (headset.poorSignal))

_thread.start_new_thread(startFileWriter, (headset, args.max_time, eeg_location, is_video_ready))
start_video_recording(start_time, args.max_time, video_location, is_video_ready)

headset.stop()
