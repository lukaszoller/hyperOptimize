import numpy as np

class HyperParamsObj():

    def __init__(self):
        self.nbrOfFeatures = 0
        self.hiddenUnitsArray = 0
        self.activationArray = 0
        self.dropOutArray = 0
        self.lossFunction = ''
        self.modelOptimizer = ''
        self.learningRate = 0
        self.learningRateDecay = 0
        self.nbrOfCategories = 0

