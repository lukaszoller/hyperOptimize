import numpy as np

class RangeForHyperParamsDict(dict):


    def __init__(self):
        self.nbrOfFeatures = 0
        self.nbrOfHiddenLayersDict = dict({'min': 0, 'max': 0})
        self.nbrOfHiddenUnitsDict = dict({'min': 0, 'max': 0})
        self.activationArray = np.array()
        self.dropOutArray = np.array()
        self.lossFunctionArray = np.array()
        self.modelOptimizerArray = np.array()
        self.learningRateDict = dict({'lrMin': 0, 'lrMax': 0})
        self.learningRateLogBool = True
        self.learningRateDecayDict = dict({'lrMin': 0, 'lrMax': 0})

