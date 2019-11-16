#coding: latin-1

import thread
from video_writer import startVideoRecording
import time, datetime, mindwave
import threading
from raw_data_writer import startFileWriter
import argparse

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required .dat file location argument
parser.add_argument('--file_id', help='A required file id to output raw data')

# Parse srguments
args = parser.parse_args()

# Threading condition to start both video and data writers
video_ready = threading.Condition()

# Max time to run the collector
collector_max_seconds = 30 # 30 seconds

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')
time.sleep(2)

start_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

while (headset.poor_signal > 5):
  print 'Headset signal noisy %d. Adjust the headset to adjust better to your forehead.' % (headset.poor_signal)
thread.start_new_thread(startFileWriter, (headset, start_time, args.file_id, video_ready, collector_max_seconds))
startVideoRecording(start_time, './data/raw/videos/' + args.file_id, video_ready, collector_max_seconds)
headset.stop()


# Leer argumentos y decidir modo de operación

# Modo natural
# Iniciar conexión a vincha, cuando se estabiliza iniciar video y toma de datos.
# Tomar datos por 3 minutos, guardar y salir.



