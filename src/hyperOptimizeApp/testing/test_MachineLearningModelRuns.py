import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj

"""This script create a model, trains, and tests it. If the overall success is high the model should predict 
correctly."""

#####################################################################################
# Prepare data
#####################################################################################


nbrOfCategories = 10
# Get data
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Reshape data (cases, features)
shapeXtrain = np.shape(x_train)
shapeXtest = np.shape(x_test)
x_train = np.reshape(x_train, (shapeXtrain[0], shapeXtrain[1] * shapeXtrain[2]))
x_test = np.reshape(x_test, (shapeXtest[0], shapeXtest[1] * shapeXtest[2]))

# Preprocess class labels (Code from: https://elitedatascience.com/keras-tutorial-deep-learning-in-python)
y_train = np_utils.to_categorical(y_train, nbrOfCategories)
y_test = np_utils.to_categorical(y_test, nbrOfCategories)

# Rescale data 0 < data < 1
x_train, x_test = x_train / 255.0, x_test / 255.0

#####################################################################################
# Create model
#####################################################################################

nbrOfNodesArray = [784, 30, 30, 10]
activationFunction = 'sigmoid'
dropOutRate = 0.01
lossFunction = 'binary_crossentropy'
modelOptimizer = 'Adam'
learningRate = 0.001
decay = 1e-6

hyperParamsObj = HyperParamsObj()
hyperParamsObj.nbrOfNodesArray = nbrOfNodesArray
hyperParamsObj.activationFunction = activationFunction
hyperParamsObj.dropOutRate = dropOutRate
hyperParamsObj.lossFunction = lossFunction
hyperParamsObj.modelOptimizer = modelOptimizer
hyperParamsObj.learningRate = learningRate
hyperParamsObj.learningRateDecay = decay

model = MachineLearningModel(hyperParamsObj, modelName='', modelId=0, model=tf.keras.models.Sequential())

model.createNetwork()

#####################################################################################
# Train and evaluate model
#####################################################################################
# train model
    # last parameter = batch size
model.trainNetwork(x_train, y_train)

# evaluate model
model.evaluateModel(x_test, y_test)

#####################################################################################
# Predict with test data
#####################################################################################
# predict data
y_predict = model.predict(x_test)
y_PredictOneCol = np.argmax(y_predict, axis=1)
y_TestOneCol = np.argmax(y_test, axis=1)

yNbrRows = np.shape(y_TestOneCol)[0]
comparisonArray = y_PredictOneCol ==y_TestOneCol
successSum = np.sum(comparisonArray)


print(str(successSum) + " rows from " + str(yNbrRows) + " rows are falsely categorized.")
successRate = successSum / yNbrRows
print("Success error: " + str(successRate) + "%")


