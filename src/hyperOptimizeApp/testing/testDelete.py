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


my_data = np.genfromtxt('E:/mnist_train.csv', delimiter=',')
