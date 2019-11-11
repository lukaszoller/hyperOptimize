import copy
import numpy as np
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
import random
import matplotlib.pyplot as plt
import multiprocessing
import cpuinfo
import csv

d = np.genfromtxt('estTimeData.csv', delimiter=',', skip_header=False)
y = d[:, -1]
x = d[:, 0:len(d[1, :]) - 1]
print("x: ", x)
print("y: ", y)


