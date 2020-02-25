# coding: latin-1
import argparse
import csv
import pickle
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

print(model)
# print(model.predict(np.array([1000,1050,1500,1050,1050,1050,1050,1050,1500,1000]).reshape(1,-1)))

# levantar buffer configurado con length (usar implementacion dequeue que tiene definido el lenght y demas)

# levantar y calibrar vincha

# antes foreach precargar buffer con los primeros 50 inputs

# teniendo 50 inputs, empezamos un foreach en el cual cada vez que ingresa un dato, lo encolamos (automaticamente se desencola el 50)

# luego feedeamos el buffer al modelo y decimos segun el % de certitud si o no. (definir por param cuanta certitud aceptamos)

# leer input por una q para abortar programa else volver al principio del foreach