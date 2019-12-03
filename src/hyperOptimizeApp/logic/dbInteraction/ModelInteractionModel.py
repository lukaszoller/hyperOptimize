from src.hyperOptimizeApp.persistence.DatabaseConnector import DatabaseConnector
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel


class ModelInteractionModel:

    def __init__(self):
        self.projectDB = DatabaseConnector()
        self.lastModel = None

    def getModelsByProjectId(self, projectId):
        return self.projectDB.getAllModelsByProjectId(projectId)

    def deleteModelsByProjectId(self, projectId):
        self.projectDB.deleteModelsByProjectId(projectId)

    def addModelByProjectId(self, modelName, projectId):
        hyperParams = HyperParamsObj()
        model = MachineLearningModel(hyperParams, modelName)
        self.projectDB.saveModel(modelName, model, projectId)
        self.lastModel = model
