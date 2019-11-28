from datetime import datetime
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository

import copy
import numpy as np
import tensorflow as tf
import numpy as np
import random
import matplotlib.pyplot as plt
import multiprocessing
import cpuinfo
import csv
from tkintertable import TableCanvas, TableModel
from tkinter import *
import random
from collections import OrderedDict
pathToData = "testDataForLoadData.csv"
firstRowIsHeader = True
firstColIsRownbr = False
nbrOfCategories = 1
dataIsForTraining = True
fl = FileSystemRepository()
data = fl.loadDataForTrainingOrPrediction(pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories, dataIsForTraining)
print(np.shape(data))