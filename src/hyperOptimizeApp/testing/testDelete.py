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

la = list([1, 2,3])

print(la)

print(la.__getitem__(len(la)-1))

lb = list()

print(not lb)