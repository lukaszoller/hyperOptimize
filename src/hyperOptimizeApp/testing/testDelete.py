import copy
import numpy as np
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
import random
import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7]
y1 = [1,2,3,4,5,6,7]
y2 = [9,8,7,6,5,4,3]

plt.subplot(121)  #sublot(Anzahl Zeilen Anzahl Spalten Bild Nummer)
plt.plot(x, y1)
plt.title('Sinus')
plt.xlim([0,2*np.pi])

plt.subplot(122)
plt.plot(x, y2)
plt.title('Cosinus')
plt.xlim([0,2*np.pi])

plt.show()