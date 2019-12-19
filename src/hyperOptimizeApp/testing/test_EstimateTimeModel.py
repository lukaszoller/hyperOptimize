
from unittest import TestCase
import numpy as np
from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository


class EstimateTimeModelTester():

    def test_estimateTime(self):  # Code mostly from https://realpython.com/linear-regression-in-python/
        """Function has not been updated. Does not work due to change in other functions."""

        # create hyperParamsObjList from estTimeData
        fl = FileSystemRepository()
        hyperParamsData, timeMeasurements = fl.getEstTimeData()
        print(hyperParamsData)
        nbrOfModels = np.shape(hyperParamsData)[0]
        hyperParamsObjList = list()
        for i in range(0, nbrOfModels):
            h = HyperParamsObj()
            nbrOfLayers = hyperParamsData[i, 0]
            nbrOfNodesPerLayer = hyperParamsData[i,1]
            learningRate = hyperParamsData[i,2]
            h.nbrOfNodesArray = np.repeat(nbrOfLayers, nbrOfNodesPerLayer)
            h.learningRate = learningRate
            hyperParamsObjList.append(h)

        estimateTimeModel = EstimateTimeModel()
        timeEstimation = estimateTimeModel.estimateTime(hyperParamsObjList)
        print("Time estimation:", timeEstimation)
        print("Sum of measurements from training data:", sum(timeMeasurements))


estimateTimeModelTester = EstimateTimeModelTester()
estimateTimeModelTester.test_estimateTime()