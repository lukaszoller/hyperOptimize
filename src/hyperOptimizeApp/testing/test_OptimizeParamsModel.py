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


class TestOptimizeParamsModel():

    def test_createHyperParamsListRandom(self):
        rangeForHyperParamsObj = RangeForHyperParamsObj()
        rangeForHyperParamsObj.dropOutDict = {'min': 0, 'max': 1}
        rangeForHyperParamsObj.activationArray = np.array(['sigmoid', 'elu', 'softmax'])
        rangeForHyperParamsObj.lossFunctionArray = np.array(['binary_crossentropy'])
        rangeForHyperParamsObj.modelOptimizerArray = np.array(['Adam'])
        rangeForHyperParamsObj.nbrOfFeatures = 784
        rangeForHyperParamsObj.learningRateDecayDict = {'min': 1e-7, 'max': 1e-5}
        rangeForHyperParamsObj.learningRateDict = {'min': 1e-5, 'max': 1e-1}
        rangeForHyperParamsObj.learningRateLogBool = True
        rangeForHyperParamsObj.nbrOfHiddenLayersDict = {'min': 1, 'max': 50}
        rangeForHyperParamsObj.nbrOfHiddenUnitsDict = {'min': 5, 'max': 100}
        rangeForHyperParamsObj.nbrOfCategories = 10

        nbrOfModels = 200

        optimizeParamsModel = OptimizeParamsModel(1,2,3,4)
        hyperParamsObjList = optimizeParamsModel.createHyperParamsListRandom(rangeForHyperParamsObj, nbrOfModels)

        i = 1
        for h in hyperParamsObjList:
            print("############################### HyperParamsObj nbr", i, "#################################")
            print(h.nbrOfNodesArray)
            print(h.activationFunction)
            i = i + 1

        return hyperParamsObjList

    def test_evaluateModels(self, hyperParamsObjList):
        #####################################################################
        # Get data
        #####################################################################
        nbrOfCategories = 10
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

        optimizeParamsModel = OptimizeParamsModel(x_train, y_train, x_test, y_test)
        optimizeParamsModel.evaluateModels(hyperParamsObjList)

        for i in range(0, len(hyperParamsObjList)):
            print("################################## Model", i+1, "##################################")
            print("Running time: ", optimizeParamsModel.runningTimeList[i])
            print("Success rate: ", optimizeParamsModel.successRate[i])
            print("Estimated time: ", )

        #  Create result data in optimizeParamsModel
        optimizeParamsModel.getResultData()

        # Visualize nbrOfLayersError
        optimizeParamsModel.visualizeHyperparamsPerformance()



testOptimizeParamsModel = TestOptimizeParamsModel()
hyperParamsObjList = testOptimizeParamsModel.test_createHyperParamsListRandom()
testOptimizeParamsModel.test_evaluateModels(hyperParamsObjList)
