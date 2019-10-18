
from unittest import TestCase
import numpy as np
from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj

class EstimateTimeModelTester():

    def test_estimateTime(self):  # Code mostly from https://realpython.com/linear-regression-in-python/
        # create hyperParamsObjList
        hyperParamsObjList = list()
        for i in range(0, 10):
            h = HyperParamsObj()
            h.nbrOfNodesArray = np.full(4, 3)
            h.learningRate = 5
            hyperParamsObjList.append(h)

        estimateTimeModel = EstimateTimeModel()
        timeEstimation = estimateTimeModel.estimateTime(hyperParamsObjList)
        print("Time estimation:", timeEstimation)


estimateTimeModelTester = EstimateTimeModelTester()
estimateTimeModelTester.test_estimateTime()