import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
from matplotlib import pyplot as plt
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from keras.utils.np_utils import to_categorical
import collections
from keras.utils import plot_model
import pydot

#####################################################################################
# 0. Prepare data
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
# 1. Create a RangeForHyperParamsDict
#####################################################################################
rangeForHyperParamsObj = RangeForHyperParamsObj()
rangeForHyperParamsObj.dropOutDict = {'min':0, 'max':1}
rangeForHyperParamsObj.activationArray = np.array(['sigmoid'])
rangeForHyperParamsObj.lossFunctionArray = np.array(['binary_crossentropy'])
rangeForHyperParamsObj.modelOptimizerArray = np.array(['Adam'])
rangeForHyperParamsObj.nbrOfFeatures = shapeXtrain[1]
rangeForHyperParamsObj.learningRateDecayDict = {'min': 1e-7, 'max':1e-5}
rangeForHyperParamsObj.learningRateDict = {'min':1e-5, 'max':1e-1}
rangeForHyperParamsObj.learningRateLogBool = True
rangeForHyperParamsObj.nbrOfHiddenLayersDict = {'min':1, 'max':50}
rangeForHyperParamsObj.nbrOfHiddenUnitsDict = {'min': 5, 'max':50}

nbrOfModels = 10

#####################################################################################
# 2. Create a hyperParamsList (a list of dicts, each with hyperparams for one model)
#####################################################################################
optimizeParamsModel = OptimizeParamsModel(x_train, y_train, x_test, y_test)
hyperParamsList = optimizeParamsModel.createHyperParamsListRandom(rangeForHyperParamsObj, nbrOfModels)
for i in hyperParamsList:
    print(i, " --- ", i.hiddenUnitsArray)

#####################################################################################
# 3. Build, train, evauluate models with the hyperParamsList
#####################################################################################

optimizeParamsModel.evaluateModels(hyperParamsList)

#####################################################################################
# 4. Print and plot some results
#####################################################################################
print(optimizeParamsModel.runningTimeArray)
print(optimizeParamsModel.errorArray)