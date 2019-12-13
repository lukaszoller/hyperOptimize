import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
from matplotlib import pyplot as plt
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import createHyperParamsListRandom
import collections
from keras.utils import plot_model
import pydot

#####################################################################################
# 0. Prepare data
#####################################################################################


class TestOptimizeParamsModel():
    """Checks if the core of the application (choose random params from range, build models, train and test models) runs."""



    def test_createHyperParamsListRandom(self):
        rangeForHyperParamsObj = RangeForHyperParamsObj()
        rangeForHyperParamsObj.dropOutDict = {'min': 0, 'max': 1}
        rangeForHyperParamsObj.activationArray = np.array(['sigmoid', 'elu', 'softmax'])
        rangeForHyperParamsObj.lossFunctionArray = np.array(['binary_crossentropy', 'mean_squared_error', 'mean_squared_logarithmic_error', 'hinge'])
        rangeForHyperParamsObj.modelOptimizerArray = np.array(['Adam', 'SGD', 'Adagrad', 'Adadelta'])
        rangeForHyperParamsObj.nbrOfFeatures = 784
        rangeForHyperParamsObj.learningRateDecayDict = {'min': 1e-7, 'max': 1e-5}
        rangeForHyperParamsObj.learningRateDict = {'min': 1e-5, 'max': 1e-1}
        rangeForHyperParamsObj.learningRateLogBool = True
        rangeForHyperParamsObj.nbrOfHiddenLayersDict = {'min': 1, 'max': 50}
        rangeForHyperParamsObj.nbrOfHiddenUnitsDict = {'min': 5, 'max': 100}
        rangeForHyperParamsObj.nbrOfCategories = 10

        nbrOfModels = 40

        hyperParamsObjList = createHyperParamsListRandom(rangeForHyperParamsObj, nbrOfModels)

        i = 1
        for h in hyperParamsObjList:
            print("############################### HyperParamsObj nbr", i, "#################################")
            print(h.nbrOfNodesArray)
            print(h.activationFunction)
            i = i + 1

        return hyperParamsObjList, rangeForHyperParamsObj, nbrOfModels

    def test_evaluateModels(self, hyperParamsObjList, nbrOfModels):
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

        optimizeParamsModel = OptimizeParamsModel(x_train, y_train, x_test, y_test, rangeForHyperParamsObj, nbrOfModels)
        optimizeParamsModel.evaluateModels()

        for i in range(0, len(hyperParamsObjList)):
            print("################################## Model", i+1, "##################################")
            print("Running time: ", optimizeParamsModel.runningTimeList[i])
            print("Success rate: ", optimizeParamsModel.successRateList[i])
            print("Estimated time: ", )

        # Visualize nbrOfLayersError
        optimizeParamsModel.visualizeHyperparamsPerformance()



testOptimizeParamsModel = TestOptimizeParamsModel()
hyperParamsObjList, rangeForHyperParamsObj, nbrOfModels = testOptimizeParamsModel.test_createHyperParamsListRandom()
testOptimizeParamsModel.test_evaluateModels(hyperParamsObjList, nbrOfModels)
