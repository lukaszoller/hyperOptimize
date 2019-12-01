from distutils.core import  setup
import py2exe
import numpy as np
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository


a = 1>=0
print(a)

nbrOfCategories = 2
nbrOfCols = 20
dataIsForTraining = True

a = (nbrOfCategories >= nbrOfCols)
b = (nbrOfCategories == 0)
c = dataIsForTraining and (nbrOfCategories >= nbrOfCols or nbrOfCategories == 0)

print(a)
print(b)
print(c)