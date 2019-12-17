from abc import ABC, abstractmethod
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository

class LoadDataModel:
    pathToDataSet = None
    firstRowIsTitle = None
    firstColIsRowNbr = None
    trainRowNumber = None
    nbrOfCategories = None
    dataIsForTraining = None

    def __init__(self, firstRowIsTitle=None, firstColIsRowNbr=None, trainRowNumber=None, nbrOfCategories=None,
                 pathToDataSet=None, dataIsForTraining=None):
        self.pathToDataSet = pathToDataSet
        self.firstRowIsTitle = firstRowIsTitle
        self.firstColIsRowNbr = firstColIsRowNbr
        self.trainRowNumber = trainRowNumber
        self.nbrOfCategories = nbrOfCategories
        self.dataIsForTraining = dataIsForTraining
        self.data = None

    def loadData(self):
        """Wrapper function for loadDataForTrainingOrPrediction() from FileSystemRepository"""
        fl = FileSystemRepository()
        try:
            x, y, rawData = fl.loadDataForTrainingOrPrediction(self.pathToDataSet, self.firstRowIsTitle,
                                                               self.firstColIsRowNbr, self.trainRowNumber,
                                                               self.nbrOfCategories, self.dataIsForTraining)
            self.data = x, y, rawData
        except ValueError:
            print("FileSystemRepository.loadDataForTrainingOrPrediction has raised an error. Wrong input for nbrOfCategories.")
            raise ValueError

    def saveData(self):
        """This method saves data to a model."""
        print("Empty method: LoadDataModel.saveData")

