class DatabaseModelModel:

    modelId = None
    modelName = ""
    hyperParams = ""
    model = ""
    projectId = 0

    def __init__(self, modelId=int, hyperParams=str, model=str, projectId=int, name=str):
        self.modelId = modelId
        self.hyperParams = hyperParams
        self.modelObject = model
        self.projectId = projectId
        self.modelName = name

    def getModelName(self):
        return self.modelName
