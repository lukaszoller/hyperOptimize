from abc import ABC, abstractmethod
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository


class LoadDataModel:
    def __init__(self):
        self.firstRowIsTitle = None
        self.firstColumnAreColNumbers = None
        self.nbrOfFeatures = None
        self.pathToDataset = None
        self.data = None

    def loadData(self, pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories, dataIsForTraining=True):
        """Wrapper function for loadDataForTrainingOrPrediction() from FileSystemRepository"""
        fl = FileSystemRepository()
        try:
            x, y, rawData = fl.loadDataForTrainingOrPrediction(pathToData, firstRowIsHeader, firstColIsRownbr,
                                                            nbrOfCategories, dataIsForTraining)
            self.data = x, y, rawData
        except ValueError:
            print("FileSystemRepository.loadDataForTrainingOrPrediction has raised an error. Wrong input for nbrOfCategories.")
            raise ValueError


    def saveData(self):
        """This method saves data to a model."""
        print("Empty method: LoadDataModel.saveData")

    def firstRowIsTitle(self):
        """This method needs a boolean value."""
        print("Empty method: LoadDataModel.firstRowIsTitle")

    def firstColumnAreColNumbers(self):
        """This method needs a boolean value."""
        print("Empty method: LoadDataModel.firstColumnAreColNumbers")
