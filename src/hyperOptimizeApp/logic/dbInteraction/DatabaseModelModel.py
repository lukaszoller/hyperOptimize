from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj


class DatabaseModelModel:

    modelId = None
    modelName = ""

    def __init__(self, modelId=int, hyperParams=HyperParamsObj, model=OptimizeParamsModel, projectId=int):
        self.modelId = modelId
        self.hyperParams = hyperParams
        self.modelObject = model
        self.projectId = projectId
