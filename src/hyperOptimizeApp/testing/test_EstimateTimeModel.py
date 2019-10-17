
from unittest import TestCase
import numpy as np
from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj

class EstimateTimeModelTester(TestCase):

    def test_hyperParamsListToData(self):
        # Create List with hyperParamsObj
        l = list()
        for i in range(0,10):
            h = HyperParamsObj()
            h.nbrOfNodesArray = np.full(i+1, (i+1*2))
            h.learningRate = (i+1)*3
            l.append(h)

        e = EstimateTimeModel()
        x = e.hyperParamsListToData(l)
        print(x)
        xCompare = np.tile([1,2,3], [10,1])
        print(xCompare)
        self.assertTrue(x, xCompare)
