import numpy as np

class RangeForHyperParamsObj():

    def __init__(self):
        self.nbrOfFeatures = 0
        self.nbrOfHiddenLayersDict = dict({'min': 0, 'max': 0})
        self.nbrOfHiddenUnitsDict = dict({'min': 0, 'max': 0})
        self.activationArray = 0 #= np.array()
        self.dropOutDict = 0#= np.array()
        self.lossFunctionArray = 0  #= np.array()
        self.modelOptimizerArray = 0 #= np.array()
        self.learningRateDict = dict({'lrMin': 0, 'lrMax': 0})
        self.learningRateLogBool = True
        self.learningRateDecayDict = dict({'lrMin': 0, 'lrMax': 0})
        self.nbrOfCategories = 0
