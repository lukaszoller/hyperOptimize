from distutils.core import  setup
import py2exe
import numpy as np
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository
import tensorflow as tf
from tensorflow.python.keras.utils import np_utils
import time


strTime = time.strftime('%H:%M:%S', time.gmtime(3600))
s = time.strptime(strTime, '%H:%M:%S')

print(s)