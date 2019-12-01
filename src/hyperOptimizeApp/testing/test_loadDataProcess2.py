from unittest import TestCase
import numpy as np
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository
from src.hyperOptimizeApp.logic.LoadDataModel import LoadDataModel

class TestLoadDataProcess(TestCase):

    def test_loadDataProcess(self):
        sumShape = 120
        path = "C:/Users/hrkun/PycharmProjects/hyperOptimize/src/hyperOptimizeApp/testing/testDataForLoadData.csv"

        # Check load with whole path
        data = np.genfromtxt(path, delimiter=",")
        print("np.genfromtxt: ", np.shape(data))
        self.assertEqual(sum(np.shape(data)), sumShape)

        # Check load with Filerepository
        fl = FileSystemRepository()
        firstRowIsHeader = False
        firstColIsRownbr = False
        nbrOfCategories = 2
        dataIsForTraining = True

        x, y, rawData = fl.loadDataForTrainingOrPrediction(path, firstRowIsHeader, firstColIsRownbr, nbrOfCategories,
                                                           dataIsForTraining)
        print("Filerepository: ", np.shape(rawData))
        self.assertEqual(sum(np.shape(rawData)), sumShape)

        # Check load with LoadDataModel
        loadDataModel = LoadDataModel()
        loadDataModel.loadData(path, firstRowIsHeader, firstColIsRownbr, nbrOfCategories, dataIsForTraining)
        x, y, rawData2 = loadDataModel.data

        print("LoadDataModel: ", np.shape(rawData2))
        self.assertEqual(sum(np.shape(rawData2)), sumShape)

