import copy
import numpy as np
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
import random

# http://faroit.com/keras-docs/1.2.0/getting-started/sequential-model-guide/



mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()



y_train = np_utils.to_categorical(y_train, 10)
y_test = np_utils.to_categorical(y_test, 10)
p = np.zeros((10000,10))

e = y_test != p
print(e[0:4])

print(np.sum(e))
