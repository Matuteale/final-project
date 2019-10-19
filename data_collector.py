#coding: latin-1

import thread
from video_writer import startVideoRecording
import time, datetime, mindwave
import sys, select
import threading

videoReady = threading.Condition()

def startFileWriter(headset, st):
  filename = './data/raw/eeg.'+st+'.dat'
  f = open(filename, 'w')

  videoReady.acquire()
  videoReady.wait()
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S-%f')
  print(st)
    
  while True:
    input = select.select([sys.stdin], [], [], 0)[0]
    if input:
      print('Exiting...!')
      break
    
    time.sleep(.01)
    (count, eeg) = (headset.count, headset.raw_value)
    print(eeg)

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S.%f')
    f.write( str(st) + ' ' + str(eeg) + ' ' + ' ' + '\n')
  f.close()

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')
time.sleep(2)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

try:
  while (headset.poor_signal > 5):
    print 'Headset signal noisy %d. Adjust the headset to adjust better to your forehead.' % (headset.poor_signal)
  thread.start_new_thread(startFileWriter, (headset, st))
  startVideoRecording('./data/raw/videos/output', videoReady)
finally:
  headset.stop()


# startVideoRecording('./data/raw/videos/output', 'q')

# Leer argumentos y decidir modo de operación

# Modo natural
# Iniciar conexión a vincha, cuando se estabiliza iniciar video y toma de datos.
# Tomar datos por 3 minutos, guardar y salir.



