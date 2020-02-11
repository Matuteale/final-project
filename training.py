#coding: latin-1

from sklearn.linear_model import LogisticRegression

print('reading training data...')
training_dataset = []
training_dataset_result = []
training_row = []
currentState = 'lookingForFalse'

# ver de saltear los ptimeros 20
with open('data/raw/training_data_v2.csv') as inputfile:
  for row in csv.reader(inputfile):
    value = row[1]
    isBlink = row[2]
    if currentState == 'lookingForFalse':
      if isBlink == False:
        currentState = 'readingFalse'
        training_row.clear()
        training_row.append(value)
    elif currentState == 'lookingForTrue': 
      if isBlink == True:
        currentState = 'readingTrue'
        training_row.clear()
        training_row.append(value)
    elif currentState == 'readingFalse': 
      if len(training_row) == 10:
        training_dataset.append(training_row)
        training_dataset_result.append(False)
        currentState = 'lookingForTrue'
      elif isBlink == True:
        currentState = 'lookingForFalse'
      else:
        training_row.append(value)
    elif currentState == 'readingTrue': 
      if len(training_row) == 10:
        training_dataset.append(training_row)
        training_dataset_result.append(True)
        currentState = 'lookingForFalse'
      else:
        training_row.append(value)

if training_dataset_result % 2 != 0:
  training_dataset.pop()
  training_dataset_result.pop()

trainedLogisticRegression = LogisticRegression(random_state=0, solver='liblinear').fit(training_dataset, training_dataset_result)

# print(fitted.predict(np.array([0,0,0,0,0,0,0,0,0,0]).reshape(1,-1)))