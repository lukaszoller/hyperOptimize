from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel

class OptimizeParamsModel:

    def __init__(self):
        self.hyperParams = dict()

    def setHyperParams(self, paramsDictionary):
        self.hyperParams = paramsDictionary


    def estimateTime(self):
        return EstimateTimeModel.estimateTime(hyperParams=self.hyperParams)

    def optimize(self):
        print("Empty method: OptimizeParamsModel.optimize")
