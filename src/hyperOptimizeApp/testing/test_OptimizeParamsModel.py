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
        rangeForHyperParamsObj.activationArray = np.array(['sigmoid', 'someActivationFunction'])
        rangeForHyperParamsObj.lossFunctionArray = np.array(['binary_crossentropy'])
        rangeForHyperParamsObj.modelOptimizerArray = np.array(['Adam'])
        rangeForHyperParamsObj.nbrOfFeatures = 20
        rangeForHyperParamsObj.learningRateDecayDict = {'min': 1e-7, 'max': 1e-5}
        rangeForHyperParamsObj.learningRateDict = {'min': 1e-5, 'max': 1e-1}
        rangeForHyperParamsObj.learningRateLogBool = True
        rangeForHyperParamsObj.nbrOfHiddenLayersDict = {'min': 1, 'max': 50}
        rangeForHyperParamsObj.nbrOfHiddenUnitsDict = {'min': 5, 'max': 50}
        rangeForHyperParamsObj.nbrOfCategories = 10

        nbrOfModels = 10

        optimizeParamsModel = OptimizeParamsModel(1,2,3,4)
        hyperParamsObjList = optimizeParamsModel.createHyperParamsListRandom(rangeForHyperParamsObj, nbrOfModels)

        i = 1
        for h in hyperParamsObjList:
            print("############################### HyperParamsObj nbr", i, "#################################")
            print(h.hiddenUnitsArray)
            print(h.activationArray)
            i = i + 1

testOptimizeParamsModel = TestOptimizeParamsModel()
testOptimizeParamsModel.test_createHyperParamsListRandom()