from src.hyperOptimizeApp.persistence.ProjectDatabase import ProjectDatabase

class ModelInteractionModel:

    def __init__(self):
        self.projectDB = ProjectDatabase()

    def getModelsByProjectId(self, projectId):
        return ProjectDatabase.getAllModelsByProjectId(projectId)