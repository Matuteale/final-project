# coding: latin-1
import argparse
import pickle
from collections import deque
import time, mindwave
import cv2
from plotter import Plotter

import numpy as np
from sklearn.linear_model import LogisticRegression

print('starting the predictive magic...')

# Instantiate the arguments parser
parser = argparse.ArgumentParser()

# Required .dat file location argument
parser.add_argument('--model', help='Path to AI model')

# Parse srguments
args = parser.parse_args()

# levantar modelo guardadod e la fase 3
model = pickle.load(open(args.model, 'rb'))

# print(model)
# print(model.predict(np.array([1000,1050,1500,1050,1050,1050,1050,1050,1500,1000]).reshape(1,-1)))

# levantar buffer configurado con length (usar implementacion dequeue que tiene definido el lenght y demas)
## usamos append para q agregue a la derecha siempre,,,el param bufferSize va a hacer que automatico popee de right cuando se llena
buffer = deque([], 50)

# levantar y calibrar vincha
headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA','ef47')
print("Hold Still...")
time.sleep(1)
print("Wait for it...")
time.sleep(1)
while (headset.poor_signal > 5):
    pass
print("Lets do this!")
plotter = Plotter(500,-500,500)
# antes foreach precargar buffer con los primeros 50 inputs
while len(buffer) < buffer.maxlen:
    (count, eeg) = (headset.count, headset.raw_value)
    plotter.plotdata([eeg])
    buffer.append(eeg)
    time.sleep(.01)


# teniendo 50 inputs, empezamos un foreach en el cual cada vez que ingresa un dato, lo encolamos (automaticamente se desencola el 50)
counter = 0
blinking = False
while True:
    #predict buffer
    if model.predict(np.array(buffer).reshape(1, -1)): #TODO maquina de estados para tomar todo el blink como un solo print
        if not blinking:
            print(buffer)
            print("BLINK " + str(counter))
            blinking = True
            counter += 1
    else:
        blinking = False

    #append next value to buffer
    (count, eeg) = (headset.count, headset.raw_value)
    plotter.plotdata([eeg])
    buffer.append(eeg)
    time.sleep(.01)
    #check for exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Exiting..')
        break



# luego feedeamos el buffer al modelo y decimos segun el % de certitud si o no. (definir por param cuanta certitud aceptamos)

# leer input por una q para abortar programa else volver al principio del foreach



# EXIT cleanup TODO
headset.stop()
