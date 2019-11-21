
class ModelModel:

    def __init__(self):
        self.modelInteract = ModelInteractionModel()

    def getModelList(self, projectId):
        modelList = self.modelInteract.getModelsByProjectId(projectId)
        return modelList
