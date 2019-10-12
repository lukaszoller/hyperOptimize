import numpy as np

class HyperParamsDict(dict):


    def __init__(self):
        self.nbrOfFeatures = 0
        self.hiddenUnitsArray = np.array()
        self.activationArray = np.array()
        self.dropOutArray = np.array()
        self.lossFunction = ''
        self.modelOptimizer = ''
        self.learningRate = 0
        self.learningRateDecay = 0

