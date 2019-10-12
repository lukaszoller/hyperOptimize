import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
from matplotlib import pyplot as plt
from src.hyperOptimizeApp.logic.RangeForHyperParamsDict import RangeForHyperParamsDict
from keras.utils.np_utils import to_categorical
import collections
from keras.utils import plot_model
import pydot


#####################################################################################
# 1. Create a RangeForHyperParamsDict
#####################################################################################
rangeForHyperParamsDict = RangeForHyperParamsDict()
rangeForHyperParamsDict.dropOutArray

#####################################################################################
# 2. Create a hyperParamsList (a list of dicts, each with hyperparams for one model)
#####################################################################################


#####################################################################################
# 3. Build, train, evauluate models with the hyperParamsList
#####################################################################################


#####################################################################################
# 4. Print and plot some results
#####################################################################################

