from unittest import TestCase

import numpy as np

from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader


class SaverLoaderTester():

    def test_hyperParamsListToData(self):
        # Create List with hyperParamsObj
        l = list()
        for i in range(0, 10):
            h = HyperParamsObj()
            h.nbrOfNodesArray = [3, 3, 3]
            h.learningRate = 5
            l.append(h)

        # Convert hyperParamsObjList to data
        sl = SaverLoader()
        x = sl.hyperParamsListToData(l)
        print(
            "################################# Test 1: test_hyperParamsListToData() #################################")
        print(x)
        # Create comparision array which should be identical to x
        xCompare = np.tile([3, 3, 5], [10, 1])
        print(xCompare)
        print("Sum of hyperParamsData MINUS comparisionData (should be 0): ", sum(sum(x - xCompare)))

    def test_getEstTimeData(self):
        print("################################# Test 2: test_getEstTimeData() #################################")
        sl = SaverLoader()
        (x, y) = sl.getEstTimeData()
        print("X:", x)
        print("Y:", y)

    def test_saveTimeMeasurementData(self):
        print(
            "################################# Test 3: test_saveTimeMeasurementData() #################################")

        # Create List with hyperParamsObj
        hyperParamsObjList = list()
        for i in range(0, 10):
            h = HyperParamsObj()
            h.nbrOfNodesArray = [3, 3, 3]
            h.learningRate = 5
            hyperParamsObjList.append(h)

        # Create some time measurement data
        timeMeasurement = np.full(len(hyperParamsObjList), 999)

        # Write data to csv
        sl = SaverLoader()
        sl.saveTimeMeasurementData(hyperParamsObjList, timeMeasurement)
        print(
            "################################# Test 3: test_saveTimeMeasurementData() #################################")
        print("Check manually if estTimeData.csv, has 10 new rows [1, 3, 5], [999]")
#
#
# slt = SaverLoaderTester()
# # slt.test_hyperParamsListToData()
# # slt.test_getEstTimeData()
# slt.test_saveTimeMeasurementData()


class TestSaverLoader(TestCase):

    def test_loadDataForTrainingOrPrediction(self):
        # function interface: pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories=0, dataIsForTraining=False

        # write data to file size(100x20)
        nbrOfCols = 20
        nbrOfRows = 100

        a = np.zeros((nbrOfRows,nbrOfCols))
        print(a)
        testDataForLoadData = "testDataForLoadData.csv"
        np.savetxt(testDataForLoadData, a, delimiter=',')


        sl = SaverLoader()
        ##################################################################################
        # 1. No header, no colNbrs, prediction data
        ##################################################################################
        resultData = sl.loadDataForTrainingOrPrediction(pathToData=testDataForLoadData, firstRowIsHeader=False, firstColIsRownbr=False)
        self.assertEqual(len(resultData), 2)    # if data is for prediction, function should return two datasets
        x, unmanipulatedData = resultData

        # Number of rows and cols should be the same
        self.assertEqual(sum(np.shape(x)), nbrOfRows+nbrOfCols)
        self.assertEqual(sum(np.shape(unmanipulatedData)), nbrOfRows+nbrOfCols)

        ##################################################################################
        # 2. header, colnbrs, prediction data
        ##################################################################################
        x, unmanipulatedData = sl.loadDataForTrainingOrPrediction(pathToData=testDataForLoadData, firstRowIsHeader=True,
                                                                  firstColIsRownbr=True)

        # Number of rows and cols should be the same -1
        self.assertEqual(sum(np.shape(x)), nbrOfRows-1 + nbrOfCols-1)
        self.assertEqual(sum(np.shape(unmanipulatedData)), nbrOfRows+nbrOfCols)

        ##################################################################################
        # 3. header, colnbrs, prediction data but nbrOfCategories !=0
        ##################################################################################
        x, unmanipulatedData = sl.loadDataForTrainingOrPrediction(pathToData=testDataForLoadData, firstRowIsHeader=False,
                                                                  firstColIsRownbr=True, nbrOfCategories=4, dataIsForTraining=False)
        # Number of rows should be the same, number of cols should be -1
        self.assertEqual(sum(np.shape(x)), nbrOfRows-1 + nbrOfCols)
        self.assertEqual(sum(np.shape(unmanipulatedData)), nbrOfRows + nbrOfCols)

        ##################################################################################
        # 4. header, colnbrs, nbrOfCategories = 4, data is for Training
        ##################################################################################
        nbrOfCategories = 4
        resultData = sl.loadDataForTrainingOrPrediction(pathToData=testDataForLoadData, firstRowIsHeader=True,
                                                        firstColIsRownbr=False, nbrOfCategories=nbrOfCategories, dataIsForTraining=True)
        self.assertEqual(len(resultData), 3)  # if data is for training, function should return two datasets
        x, y, unmanipulatedData = resultData

        # Number of rows and cols should be the same
        self.assertEqual(sum(np.shape(x)), nbrOfRows - 1 + nbrOfCols-nbrOfCategories) # Minus header (-1), minus categories (- nbrOfCategories)
        self.assertEqual(sum(np.shape(y)), nbrOfRows -1 + nbrOfCategories)     # Minus header (-1), plus nbrOfCategories (+ nbrOfCategories)
        self.assertEqual(sum(np.shape(unmanipulatedData)), nbrOfRows + nbrOfCols)

