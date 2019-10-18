import numpy as np

from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader


class SaverLoaderTester():

    def test_hyperParamsListToData(self):
        # Create List with hyperParamsObj
        l = list()
        for i in range(0, 10):
            h = HyperParamsObj()
            h.nbrOfNodesArray = np.full(1, 3)
            h.learningRate = 5
            l.append(h)

        # Convert hyperParamsObjList to data
        sl = SaverLoader()
        x = sl.hyperParamsListToData(l)
        print("################################# Test 1: test_hyperParamsListToData() #################################")
        print(x)
        # Create comparision array which should be identical to x
        xCompare = np.tile([1, 3, 5], [10, 1])
        print(xCompare)
        print("Sum of hyperParamsData MINUS comparisionData (should be 0): ", sum(sum(x - xCompare)))

    def test_getEstTimeData(self):
        print("################################# Test 2: test_saveTimeMeasurementData() #################################")
        sl = SaverLoader()
        (x,y) = sl.getEstTimeData()
        print("X:", x)
        print("Y:", y)

    def test_saveTimeMeasurementData(self):
        # Create List with hyperParamsObj
        hyperParamsObjList = list()
        for i in range(0, 10):
            h = HyperParamsObj()
            h.nbrOfNodesArray = np.full(1, 3)
            h.learningRate = 5
            hyperParamsObjList.append(h)

        # Create some time measurement data
        timeMeasurement = np.full(len(hyperParamsObjList), 999)

        # Write data to csv
        sl = SaverLoader()
        sl.saveTimeMeasurementData(hyperParamsObjList, timeMeasurement)
        print("################################# Test 3: test_saveTimeMeasurementData() #################################")
        print("Check manually if estTimeData.csv, has 10 new rows [1, 3, 5], [999]")


slt = SaverLoaderTester()
slt.test_hyperParamsListToData()
slt.test_getEstTimeData()
slt.test_saveTimeMeasurementData()