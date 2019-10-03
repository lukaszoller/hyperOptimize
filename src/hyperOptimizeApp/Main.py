from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.EstimateTimeModel_Advanced import EstimateTimeModel_Advanced

import os

print(os.getcwd())


e = EstimateTimeModel()
a = EstimateTimeModel_Advanced()

print(e.estimateTime([5,10,15,20]))

print(a.estimateTime([5,10,15,20]))


