from abc import ABC, abstractmethod
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository


class LoadDataModel:

    firstRowIsTitle = None
    firstColumnAreColNumbers = None
    nbrOfFeatures = None
    pathToDataSet = None

    def __init__(self, firstRowIsTitle=None, firstColumnAreColNumbers=None, nbrOfFeatures=None, pathToDataSet=None):
        self.firstRowIsTitle = firstRowIsTitle
        self.firstColumnAreColNumbers = firstColumnAreColNumbers
        self.nbrOfFeatures = nbrOfFeatures
        self.pathToDataSet = pathToDataSet
        self.data = None

    def loadData(self, pathToData, firstRowIsHeader, firstColIsRowNbr, nbrOfCategories, dataIsForTraining=True):
        """Wrapper function for loadDataForTrainingOrPrediction() from FileSystemRepository"""
        fl = FileSystemRepository()
        try:
            x, y, rawData = fl.loadDataForTrainingOrPrediction(pathToData, firstRowIsHeader, firstColIsRowNbr,
                                                            nbrOfCategories, dataIsForTraining)
            self.data = x, y, rawData
        except ValueError:
            print("FileSystemRepository.loadDataForTrainingOrPrediction has raised an error. Wrong input for nbrOfCategories.")
            raise ValueError

    def saveData(self):
        """This method saves data to a model."""
        print("Empty method: LoadDataModel.saveData")

