from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.EstimateTimeModel_Advanced import EstimateTimeModel_Advanced
from src.hyperOptimizeApp.view.MainView import MainView

import os

print(os.getcwd())


e = EstimateTimeModel()
a = EstimateTimeModel_Advanced()
mainView = MainView()

print(e.estimateTime([5, 10, 15, 20]))

estim = a.estimateTime([5, 10, 15, 20])
print(estim)

mainView.build(estim)




