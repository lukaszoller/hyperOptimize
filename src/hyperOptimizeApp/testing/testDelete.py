from datetime import datetime

import copy
import numpy as np
import tensorflow as tf
import numpy as np
import random
import matplotlib.pyplot as plt
import multiprocessing
import cpuinfo
import csv

testDataForLoadData = "testDataForLoadData.csv"
data = np.genfromtxt(testDataForLoadData, delimiter=',', skip_header=False)

m = (data,data)
print(len(m))

r, c = np.shape(data)
print((r, c))
print(sum(np.shape(data)))
print(sum(r,c))