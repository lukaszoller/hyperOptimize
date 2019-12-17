from hyperOptimizeApp.persistence.dbInteraction.ModelInteractionModel import ModelInteractionModel


class ModelModel:

    def __init__(self):
        self.modelInteract = ModelInteractionModel()

    def getModelList(self, projectId):
        modelList = self.modelInteract.getModelsByProjectId(projectId)
        return modelList
