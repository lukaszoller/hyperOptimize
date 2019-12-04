from src.hyperOptimizeApp.persistence.DatabaseConnector import DatabaseConnector
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
import json


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

    def updateModelById(self, modelId, model):
        self.projectDB.updateModelById(modelId, model)

    def getMachineLearningModelData(self):
        pass
