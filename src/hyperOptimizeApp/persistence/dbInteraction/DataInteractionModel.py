from src.hyperOptimizeApp.persistence.core.DatabaseConnector import DatabaseConnector
from src.hyperOptimizeApp.logic.LoadDataModel import LoadDataModel


class DataInteractionModel:
    def __init__(self):
        self.projectDB = DatabaseConnector()

    def getLoadDataModel(self, projectId):
        dataModel = self.projectDB.getProjectDataInformation(projectId)
        return dataModel

    def setDataForProject(self, projectId, dataModel=LoadDataModel):
        self.projectDB.updateProjectDataInformation(projectId, dataModel.pathToDataSet, dataModel.firstRowIsTitle,
                                                    dataModel.firstColIsRowNbr, dataModel.nbrOfCategories,
                                                    dataModel.trainRowNumber)
