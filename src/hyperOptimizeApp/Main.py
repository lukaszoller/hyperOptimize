from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel

import os

print(os.getcwd())


e = EstimateTimeModel()

print(e.estimateTime([1,5,0.01]))


