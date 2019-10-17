import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
from matplotlib import pyplot as plt
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader
from keras.utils.np_utils import to_categorical
import collections
from keras.utils import plot_model
import pydot

#####################################################################################
# 0. Prepare data
#####################################################################################


class SaverLoaderTester():

    def test_getEstTimeData(self):
        """Returns to arrays. A 2D array x and a 1D array y."""
        sl = SaverLoader()
        return sl.getEstTimeData()

    def saveTimeMeasurementData(self, x, y):
        np.savetxt('estTimeData.csv', [x, y], delimiter=',')


slt = SaverLoaderTester()
print(slt.test_getEstTimeData())

