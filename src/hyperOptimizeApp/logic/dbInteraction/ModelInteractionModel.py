from src.hyperOptimizeApp.persistence.DatabaseConnector import DatabaseConnector

class ModelInteractionModel:

    def __init__(self):
        self.projectDB = DatabaseConnector()

    def getModelsByProjectId(self, projectId):
        return self.projectDB.getAllModelsByProjectId(projectId)