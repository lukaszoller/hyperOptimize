from distutils.core import  setup
import py2exe
import numpy as np
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository
import tensorflow as tf
from tensorflow.python.keras.utils import np_utils
import time
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import createHyperParamsListRandom



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

nbrOfModels = 2

hyperParamsObjList = createHyperParamsListRandom(rangeForHyperParamsObj, nbrOfModels)

print("Hoi")