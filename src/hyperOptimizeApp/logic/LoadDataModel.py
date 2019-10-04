from abc import ABC, abstractmethod

class LoadDataModel(ABC):
    def __init__(self):
        pass

    def loadData(self):
        print("Empty method: LoadDataModel.loadData")

    def saveData(self):
        """This method saves data to a model."""
        print("Empty method: LoadDataModel.saveData")

    def firstRowIsTitle(self):
        """This method needs a boolean value."""
        print("Empty method: LoadDataModel.firstRowIsTitle")

    def firstColumnAreColNumbers(self):
        """This method needs a boolean value."""
        print("Empty method: LoadDataModel.firstColumnAreColNumbers")

